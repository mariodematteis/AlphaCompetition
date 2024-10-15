from api.ibapi.ibapi import App
from strategies.OOTB import OutOfTheBox


if __name__ == '__main__':
    out_of_the_box: OutOfTheBox = OutOfTheBox()
    out_of_the_box.analyze(
        time_frame='1d',
    )
    app: App = App()
