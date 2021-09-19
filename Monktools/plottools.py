import matplotlib.pyplot as plt  # To visualize


class PLOTS:
    def plot_results(self, datas_and_fits, xlabel, ylabel, title, plot_fit):
        plt.scatter(datas_and_fits[0], datas_and_fits[1])
        if plot_fit: plt.plot(datas_and_fits[0], datas_and_fits[2], color='red')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig('Plots/' + title + '.jpg')
        plt.close()

    def plot_multiple(self, datas_and_fits, x_label, y_label, plot_fit):
        for d in datas_and_fits:
            test = d[0]
            plt.scatter(test[0], test[1])
            if plot_fit:
                plt.plot(test[0], test[2], label=d[1], color='red')
