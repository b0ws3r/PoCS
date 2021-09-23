import matplotlib.pyplot as plt  # To visualize


def plot_results(datas_and_fits, xlabel, ylabel, title):
    plt.scatter(datas_and_fits[xlabel], datas_and_fits[ylabel])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig('Plots/' + title + '.jpg')
    plt.close()


def plot_results_with_fit(datas_and_fits, xlabel, ylabel, title, y_pred):
    plt.scatter(datas_and_fits[xlabel], datas_and_fits[ylabel])
    plt.plot(datas_and_fits[xlabel], y_pred, color='red')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig('Plots/' + title + '.jpg')
    plt.close()


def plot_multiple(datas_and_fits, x_label, y_label, plot_fit):
    for d in datas_and_fits:
        test = d[0]
        plt.scatter(test[0], test[1])
        if plot_fit:
            plt.plot(test[0], test[2], label=d[1], color='red')
