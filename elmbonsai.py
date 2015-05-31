from collections import namedtuple

Tick = namedtuple('Tick', ['type', 'time'])

class ReactionGroup(object):
    def __init__(self, time):
        self.groups = []
        self.time = time
        self.active = True

    def discard(self):
        self.active = False
        for group in self.groups:
            group.discard() 

    def spawn(self, signal):
        assert self.active, "inactive group"
        deploy = Deployer(self.time, [])
        deploy.one(signal)
        self.groups.append(deploy.reaction)
        return deploy.reaction

    def group(self):
        group = ReactionGroup(self.time)
        self.groups.append(group)
        return group

    def update(self, event):
        if not self.active:
            return False
        if event.type == Tick:
            self.time = event.time
        self.groups[:] = (reaction for reaction in self.groups if reaction.update(event))
        if len(self.groups) == 0:
            self.active = False
        return self.active

class Reaction(object):
    def __init__(self, time, cells):
        self.time = time
        self.cells = cells
        self.active = True

    def discard(self):
        self.active = False

    def update(self, event):
        if not self.active:
            return False
        if event.type == Tick:
            self.time = event.time
        self.active = False
        for cell in self.cells:
            cell.update(event)
        else:
            self.active = True
        return self.active

class Deployer(object):
    def __init__(self, time, cells):
        self.reaction = Reaction(time, cells)
        self.time = time
        self.cells = cells
        self.visit = {}

    def one(self, node):
        if not isinstance(node, Signal):
            node = constant(node)
        if node in self.visit:
            return self.visit[node]
        self.visit[node] = cell = node.deploy(self)
        self.cells.append(cell)
        return cell

    def many(self, nodes):
        return list(self.one(node) for node in nodes)

class Cell(object):
    def __init__(self, init):
        self.changed = False
        self.value = init

class ConstantCell(Cell):
    def __init__(self, init):
        Cell.__init__(self, init)

    def update(self, event):
        pass

class InputCell(Cell):
    def __init__(self, init, func):
        Cell.__init__(self, init)
        self.func = func

    def update(self, event):
        self.changed = self.func(self, event)

class FoldCell(Cell):
    def __init__(self, init, func, args):
        Cell.__init__(self, init)
        self.func = func
        self.args = args

    def update(self, event):
        if any(arg.changed for arg in self.args):
            value = self.func(self.value, *(arg.value for arg in self.args))
            self.changed = (self.value != value)
            self.value = value

class LiftCell(Cell):
    def __init__(self, func, args):
        Cell.__init__(self, func(*(arg.value for arg in args)))
        self.func = func
        self.args = args

    def update(self, event):
        if any(arg.changed for arg in self.args):
            value = self.func(*(arg.value for arg in self.args))
            self.changed = (self.value != value)
            self.value = value

class NowCell(Cell):
    def __init__(self, time):
        Cell.__init__(self, time)

    def update(self, event):
        if event.type == Tick:
            self.value = event.time
            self.changed = True
        else:
            self.changed = False

class AfterCell(Cell):
    def __init__(self, start):
        Cell.__init__(self, 0.0)
        self.start = start
    
    def update(self, event):
        if event.type == Tick:
            self.value = event.time - self.start
            self.changed = True
        else:
            self.changed = False

class EveryCell(Cell):
    def __init__(self, start, step):
        Cell.__init__(self, 0)
        self.start = start
        self.step = step
    
    def update(self, event):
        if event.type == Tick:
            value = int((event.time - self.start) / step)
            self.changed = value != self.value
            self.value = value

class UntilCell(Cell):
    def __init__(self, start, limit):
        Cell.__init__(self, start >= limit)
        self.start = start
        self.limit = limit
    
    def update(self, event):
        if event.type == Tick:
            value = event.time - self.start > self.limit
            self.changed = value != self.value
            self.value = value

class SampleOnCell(Cell):
    def __init__(self, control, signal):
        Cell.__init__(self, signal.value)
        self.control = control
        self.signal = signal

    def update(self, event):
        if self.control.changed:
            self.value = self.signal.value
        self.changed = self.control.changed

class Signal(object):
    pass

class Input(Signal):
    def __init__(self, intro, func):
        self.intro = intro
        self.func = func

    def deploy(self, deploy):
        return InputCell(self.intro(deploy.reaction), self.func)

class foldp(Signal):
    def __init__(self, func, init, *args):
        self.func = func
        self.init = init
        self.args = args

    def deploy(self, deploy):
        return FoldCell(
            self.init,
            self.func,
            deploy.many(self.args))

class lift(Signal):
    def __init__(self, func, *args):
        self.func = func
        self.args = args

    def deploy(self, deploy):
        return LiftCell(
            self.func,
            deploy.many(self.args))

class liftfoldp(Signal):
    def __init__(self, intro, func, *args):
        self.intro = intro
        self.func = func
        self.args = args

    def deploy(self, deploy):
        args = deploy.many(self.args)
        init = self.intro(deploy.reaction, *(arg.value for arg in args))
        return FoldCell(init, self.func, args)

class constant(Signal):
    def __init__(self, value):
        self.value = value

    def deploy(self, deploy):
        return ConstantCell(self.value)

class TimeSignal(Signal):
    def __init__(self, cls, *args):
        self.cls = cls
        self.args = args

    def deploy(self, deploy):
        return self.cls(deploy.time, *self.args)

now = TimeSignal(NowCell)
after = TimeSignal(AfterCell)

def every(step):
    return TimeSignal(EveryCell, step)

def until(limit):
    return TimeSignal(UntilCell, limit)

class sample_on(Signal):
    def __init__(self, control, signal):
        self.control = control
        self.signal = signal

    def deploy(self, deploy):
        return SampleOnCell(
            deploy.one(self.control),
            deploy.one(self.signal))
