<<<<<<< HEAD
def question1():
    
    print('The question is -: You have a pandas DataFrame df with a numeric column sales. Which option best creates a basic histogram of sales using Matplotlib?\n\nA) plt.scatter(df.index, df["sales"]) followed by plt.show()\n\nB) df["sales"].hist() followed by plt.show()\n\nC) plt.plot(df["sales"]) followed by plt.show()\n\nD) plt.bar(df.index, df["sales"]) followed by plt.show()')

    user = input('Enter your answer (A, B, C, or D): ').upper()

    if user == 'B':
        print('Correct!, you won 1000 arans')

    else:
        print('Wrong answer, and you lost 500 arans')

def question2():
    print('The second question is on your screen -: You want to compare the distributions of the numeric columns age and income in the same DataFrame df using Seaborn. Which visualization is most appropriate for quickly comparing their shapes while also seeing individual observations?\n\nA) Pair of overlapping histograms using Matplotlib plt.hist with transparency\n\nB) Seaborn heatmap of the correlation matrix using sns.heatmap(df.corr())\n\nC) Seaborn boxplot for age and income using sns.boxplot(data=df[["age", "income"]])\n\nD) Seaborn violin plot using sns.violinplot(data=df[["age", "income"]])')

    user = input('Enter your answer (A, B, C, or D): ').upper()

    if user == 'D':
        print('Correct!, you won 2000 arans')

    else:
        print('Wrong answer, and you lost 500 arans')


def question3():
    print('The third question is on your screen -: You have a long-format DataFrame df_long with columns ["country", "year", "gdp"]. You want to plot each country\'s GDP over time on the same line chart using Seaborn. Which function and mapping are most appropriate?\n\nA) sns.lineplot(data=df_long, x="year", y="gdp", hue="country")\n\nB) sns.histplot(data=df_long, x="gdp", hue="country")\n\nC) sns.scatterplot(data=df_long, x="country", y="gdp")\n\nD) sns.barplot(data=df_long, x="year", y="gdp", hue="country")')
    user = input('Enter your answer (A, B, C, or D): ').upper()

    if user == 'A':
        print('Correct!, you won 3000 arans')

    else:
        print('Wrong answer, and you lost 500 arans')


if __name__ == "__main__":
    print('Welcome to the quiz game! You will be asked two questions about data visualization. Answer correctly to win arans, but be careful - a wrong answer will end the game. Good luck!\n')

    question1()
    question2()
=======
def question1():
    
    print('The question is -: You have a pandas DataFrame df with a numeric column sales. Which option best creates a basic histogram of sales using Matplotlib?\n\nA) plt.scatter(df.index, df["sales"]) followed by plt.show()\n\nB) df["sales"].hist() followed by plt.show()\n\nC) plt.plot(df["sales"]) followed by plt.show()\n\nD) plt.bar(df.index, df["sales"]) followed by plt.show()')

    user = input('Enter your answer (A, B, C, or D): ').upper()

    if user == 'B':
        print('Correct!, you won 1000 arans')

    else:
        print('Wrong answer, and you lost 500 arans')

def question2():
    print('The second question is on your screen -: You want to compare the distributions of the numeric columns age and income in the same DataFrame df using Seaborn. Which visualization is most appropriate for quickly comparing their shapes while also seeing individual observations?\n\nA) Pair of overlapping histograms using Matplotlib plt.hist with transparency\n\nB) Seaborn heatmap of the correlation matrix using sns.heatmap(df.corr())\n\nC) Seaborn boxplot for age and income using sns.boxplot(data=df[["age", "income"]])\n\nD) Seaborn violin plot using sns.violinplot(data=df[["age", "income"]])')

    user = input('Enter your answer (A, B, C, or D): ').upper()

    if user == 'D':
        print('Correct!, you won 2000 arans')

    else:
        print('Wrong answer, and you lost 500 arans')


def question3():
    print('The third question is on your screen -: You have a long-format DataFrame df_long with columns ["country", "year", "gdp"]. You want to plot each country\'s GDP over time on the same line chart using Seaborn. Which function and mapping are most appropriate?\n\nA) sns.lineplot(data=df_long, x="year", y="gdp", hue="country")\n\nB) sns.histplot(data=df_long, x="gdp", hue="country")\n\nC) sns.scatterplot(data=df_long, x="country", y="gdp")\n\nD) sns.barplot(data=df_long, x="year", y="gdp", hue="country")')
    user = input('Enter your answer (A, B, C, or D): ').upper()

    if user == 'A':
        print('Correct!, you won 3000 arans')

    else:
        print('Wrong answer, and you lost 500 arans')


if __name__ == "__main__":
    print('Welcome to the quiz game! You will be asked two questions about data visualization. Answer correctly to win arans, but be careful - a wrong answer will end the game. Good luck!\n')

    question1()
    question2()
>>>>>>> 3f7e543e3da3f338aae73938f5603f57c2c87d25
    question3()