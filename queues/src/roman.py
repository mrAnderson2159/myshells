# import os,sys
# sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
# from debug import debug

class Roman:
    __u = ['I','II','III','IV','V','VI','VII','VIII','IX']
    __d = ['X','XX','XXX','XL','L','LX','LXX','LXXX','XC']
    __c = ['C','CC','CCC','CD','D','DC','DCC','DCCC','CM']
    __a = [__u, __d, __c]
    __v = {'numbers':['I','V','X','L','C','D','M'], 'values':[1,5,10,50,100,500,1000]}
    __v = {n: {'value':v, 'repeat': not (i % 2)} for i, (n,v) in enumerate(zip(*__v.values()))}

    @classmethod
    def to_roman(cls, number:int) -> str:
        if number >= 1000:
            raise ValueError("Non riesco a rappresentare numeri maggiori di 1000 nella numerazione romana")
        exp = 2
        mol = 9
        res = str()

        while number != 0:
            while number % (10 ** exp * mol) == number:
                if mol == 1:
                    mol = 9
                    exp -= 1
                else:
                    mol -= 1
            res += cls.__a[exp][mol - 1]
            number %= (10 ** exp * mol)
            exp -= 1
            mol = 9

        return res

    @classmethod
    def from_roman(cls, number:str) -> int:
        if number[0] == 'M':
            raise ValueError("Non riesco a convertire numeri romani maggiori di 1000 in numeri arabi")
        res = 0
        i = len(number) - 1
        while i >= 0:
            current = cls.__v[number[i]]['value']
            prev = cls.__v[number[i-1]]['value']
            if i and current > prev:
                res += current - prev
                i -= 2
            else:
                res += current
                i -= 1

                
        return res


# if __name__ == '__main__':
#     for i in range(1,1000):
#         r = Roman.to_roman(i)
#         print(i,r)