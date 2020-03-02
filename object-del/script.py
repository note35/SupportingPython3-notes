from __future__ import print_function


class ExampleObj:
    prop1 = False

    def __init__(self):
        print('start', ExampleObj.prop1)

    def run(self):
        ExampleObj.prop1 = True

    def __del__(self):
        if ExampleObj.prop1 == True:
            ExampleObj.prop1 = False
            # in this line
            # python3 will execute normally
            # python2 will raise AttributeError exception since the instance of ExampleObj has been deleted
            print('done', ExampleObj.prop1)


e = ExampleObj()
e.run()
