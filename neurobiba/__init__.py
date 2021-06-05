from numpy import (exp, random, array, dot, append)
from pickle import (dump, load)


class Weights(list):
    def __init__(self, size, bias=False):
        """
        size это список слоев с количеством их нейронов.
        
        bias этот флаг добавляет к каждому слою нейрон смещения
        
        Пример использования функции:
        `weights = Weights([3, 10, 10 ,2])`

        Здесь три нейрона на входном слое, 
        два промежуточных слоя по 10 нейронов и 2 нейрона на выходе.
        """ 
        self.bias = bias
        super().__init__([2*random.random((size[i]+int(bias), size[i+1])) - 1 for i in range(len(size)-1)])

    def deriv_sigmoid(self, x, alpha):
        """Производная сигмоиды. Используется для обучения."""
        return (x * (1-x))*alpha

    def sigmoid(self, x):
        """Сигмоида."""
        return 1/(1+exp(-x))

    def training(self, input_layer, correct_output, alpha=0.9):
        """
        Функция для обучения нейросети 
        методом обратного распространения ошибки.
        Меняет веса.
        Ее нужно вызывать в цикле столько раз сколько потребуется для обучения.

        Пример использования функции:
        `for i in range(1000): 
            weights.training(input_layer, correct_output)`

        `input_layer` - это список нейронов входного слоя. 
        Они должны находится в диапазоне от `0` до `1`.
        Например:
        `input_layer = [1, 0, 0.7]`

        correct_output это список правильных выходов для заданных входов.
        Они должны находится в диапазоне от `0` до `1`.
        Например:
        `correct_output = [0.5, 1]`

        `alpha` - это коэфициент скорости обучения. 
        Его оптимальное значение меняется в зависимости от задачи.
        """

        l = [array([input_layer])]
        d = len(self)

        for i in range(d):
            if self.bias:
                l[-1] = array([append(l[-1], 1)])
            l.append(self.sigmoid(dot(l[-1], self[i])))

        l_error = []
        l_delta = []

        l_error.append(correct_output - l[-1])
        l_delta.append(l_error[-1] * self.deriv_sigmoid(l[-1], alpha))

        for i in range(d-1):
            l_error.append(l_delta[i].dot(self[d-1-i].T))
            l_delta.append(l_error[-1] * self.deriv_sigmoid(l[d-1-i], alpha))

        if self.bias:
            for ind in range(d-1):
                self[ind] += l[ind].T.dot(array([l_delta[-1-ind][0][:-1]]))
            self[d-1] += l[d-1].T.dot(l_delta[-d])
        else:
            for ind in range(d):
                self[ind] += l[ind].T.dot(l_delta[-1-ind])

    def feed_forward(self, input_layer):
        """
        Функция для получения ответа нейросети.
        Возвращает список выходных нейронов.

        Пример использования:
        `result = weights.feed_forward(input_layer)`

        `input_layer` - это список входных нейронов.
        """

        l = [array([input_layer])]
        d = len(self)

        for i in range(d):
            if self.bias:
                l[-1] = array([append(l[-1], 1)])
            l.append(self.sigmoid(dot(l[-1], self[i])))

        return l[-1][0]


    def feed_reverse(self, input_layer):
        """
        НЕ РАБОТАЕТ ЕСЛИ bias==True

        Эта функция работает так же, как `feed_forward`,
        но проводит сигнал через нейросеть в обратном направлении.
        В нее в качестве входного слоя подают то, что ранее считалось выходным слоем.

        Пример использования:
        `r = weights.feed_reverse(input_layer)`
        """

        weightsr = list(reversed(self))
        for ind, i in enumerate(weightsr):
            weightsr[ind] = weightsr[ind].T

        l = [array([input_layer])]
        d = len(weightsr)

        for i in range(d):
            l.append(self.sigmoid(dot(l[-1], weightsr[i])))
        return l[-1][0]


    def download_weights(self, file_name='weights'):
        """
        Загрузка весов из файла.

        Пример использования:
        `weights.download_weights()`

        В качестве аргумента `file_name` можно указать имя файла `.dat` без указания формата.
        """

        try:
            with open(f'{file_name}.dat', 'rb') as file:
                self = load(file)
        except:
            print('no file with saved weights')


    def save_weights(self, file_name='weights'):
        """
        Схранение весов в файл.

        Пример использования:
        `weights.save_weights()`

        В качестве аргумента `file_name` можно указать имя файла `.dat` без указания формата.
        """

        with open(f'{file_name}.dat', 'wb') as file:
            dump(self, file)
        print('file saved')
