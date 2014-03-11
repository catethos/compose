# Library inspired by Clojure threading macro and monad

def meta(data):
    def __inner__(f):
        f.__meta__ = data
        return f
    return __inner__    

def compose(func):
        return lambda arg: reduce(lambda x,f:f(x),func,arg)

def compose_m(*m):
    return {"unit": compose([x["unit"] for x in m]),
            "lift": compose([x["lift"] for x in m]),
            "bind": compose([x["bind"] for x in m])}

def thread(x,*f,**monad):    
    
    try:
        kw = monad["monad"]
    except KeyError:
        kw = identity_m()
    
    bind = kw["bind"]
    lift = kw["lift"]
    unit = kw["unit"]
    
    l_f = map(lift,f)
    new_f = it.chain.from_iterable(it.izip(l_f,it.repeat(bind)))
    return compose(new_f)(unit(x))
    

def identity_m():
    def _unit(x):
        return {"_v":x}
    
    def _lift(f):
        def __inner(x):
            x["_v"] = f(x["_v"])
            return x
        return __inner
        
        
    return {"unit": _unit,
            "lift": _lift,
            "bind": ident}

def logging_m():
    def _f(x):
        print x["_v"]
        return x
    
    return {"unit":ident,
            "lift":ident,
            "bind":_f} 

def acc_m():
    def _unit(x):
        x["acc"] = []
        return x
    
    def _bind(x):
        x["acc"].append(x["_v"])
        return x
    
    return{"unit": _unit,
           "lift": ident,
           "bind": _bind}

def list_m():
    
    def _unit(f):
        return{"function":f, "_v":[]}
    def _lift(x):
        def __inner__(d):
            
            f = d["function"]
            d["_v"].append(f(x))
            return d
        return __inner__
    
        
    return{"unit": _unit,
           "lift": _lift,
           "bind": ident}                                              
                               
                            
    
