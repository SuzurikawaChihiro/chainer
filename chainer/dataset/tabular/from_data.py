import chainer
from chainer.dataset.tabular import _wrappers


def from_data(*args, **kwargs):
    """Create a :class:`~chainer.dataset.TabularDataset` from lists/arrays.

    Args:
        args (list or array or tuple): Data of a column.
            If this argument is an array or a list,
            it is treated as :obj:`data`.
            In this case, the key is generated automatically.
            Do not rely on the key.
            If this argument is a tuple, it is treated as :obj:`(key, data)`.
        kwargs (list or array): Data of a column.
            The order of columns is determined automatically.
            Do not rely on the order.
    Return:
        A :class:`~chainer.dataset.TabularDataset`.
        If only one argument is given, :attr:`mode` is :obj:`None`.
        If more than one arguments are given as :obj:`args`,
        :attr:`mode` is :class:`tuple`.
        If more than one arguments are given as :obj:`kwargs`,
        :attr:`mode` is :class:`dict`.
    """
    datasets = []

    for data in args:
        if isinstance(data, tuple):
            key, data = data
        else:
            key = '_{}'.format(id(data))

        if isinstance(data, chainer.get_array_types()):
            datasets.append(_wrappers._Array(key, data))
        elif isinstance(data, list):
            datasets.append(_wrappers._List(key, data))

    for key, data in kwargs.items():
        if isinstance(data, chainer.get_array_types()):
            datasets.append(_wrappers._Array(key, data))
        elif isinstance(data, list):
            datasets.append(_wrappers._List(key, data))

    if len(datasets) == 1:
        return datasets[0]
    elif args and kwargs:
        raise ValueError('Mixture of args and kwargs is not supported')
    elif args:
        return datasets[0].join(*datasets[1:]).as_tuple()
    elif kwargs:
        return datasets[0].join(*datasets[1:]).as_dict()
    else:
        raise ValueError('At least one data must be passed')
