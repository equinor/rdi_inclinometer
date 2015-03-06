from abc import abstractmethod


class AxisTranslator(object):
    name = None

    @abstractmethod
    def translate(self, axis0, axis1, axis2):
        pass


class AxisTranslatorA(AxisTranslator):
    name = 'A'

    def translate(self, axis0, axis1, axis2):
        return axis0, axis1, axis2


class AxisTranslatorB(AxisTranslator):
    name = 'B'

    def translate(self, axis0, axis1, axis2):
        return -axis2, axis1, axis0


translator_dict = {'A': AxisTranslatorA(),
                   'B': AxisTranslatorB()}