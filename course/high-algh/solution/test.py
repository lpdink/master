if __name__=="__main__":
    t=list(range(10))
    while len(t)!=0:
        if t.pop()==5:
            break
    else:
        print("all done.")
    print("script done.")