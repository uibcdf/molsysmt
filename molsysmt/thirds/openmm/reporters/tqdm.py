
class TQDMReporter(object):

    def __init__(self, reportInterval, total_n_steps):

        from tqdm.auto import tqdm

        self._pbar = tqdm(total=total_n_steps, position=0, leave=True)
        self._reportInterval = int(total_n_steps/reportInterval)
        if self._reportInterval==0:
            self._reportInterval=1
        self._total_n_steps = total_n_steps
        self._needsPositions = False
        self._needsVelocities = False
        self._needsForces = False
        self._needEnergy = False

    def describeNextReport(self, simulation):

        steps_left = simulation.currentStep % self._reportInterval
        steps = self._reportInterval - steps_left
        return (steps, self._needsPositions, self._needsVelocities, self._needsForces, self._needEnergy)

    def report(self, simulation, state):

        self._pbar.update(self._reportInterval)

    def finalize(self):

        self._pbar.close()

        pass

