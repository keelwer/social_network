# class Probe:
#
#     def __init__(self, market):
#         self.perr = market
#         self.lert = self.perr * 9
#
# l = Probe('345')
# print(l.lert)
import pandas

df2 = pandas.DataFrame([('parrot', 24.0, 'second'),
                        ('lion', 80.5, 1),
                        ('monkey', 80.5, None)],
                       columns=('name', 'max', 'rank'))

print(df2)
# print(df2.values)
# print(df2.columns.get_loc("max"))


# class Met:
#
#     def __init__(self, df):
#         self.values = df.values
#         self.max = self.values[df.columns.get_loc("max")]
#
#     def __call__(self):
#         return [self.values]
#
# l = Met(df2)
# print(l.max)
# # for m in l.values:
# #     print(m.max)
# # print(l.max)