class HTTPError(Exception):
    pass
def get_or_404(collection:dict,id:int)->dict:
    if id not in collection:  
        raise HTTPError("404 not fount")
    return collection[id]
tasks={


    1:{"title":"study"},
    2:{"title":"sleep"}

}
try:
    print(get_or_404(tasks,1))
    print(get_or_404(tasks,3))
except HTTPError as e:
    print(e)