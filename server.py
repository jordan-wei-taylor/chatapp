if __name__ == '__main__':
    
    # patch built in modules with safer production equivalents
    # e.g. time.sleep -> eventlet.sleep
    from eventlet import monkey_patch
    monkey_patch() 

    # host the server
    from chatapp import serve
    serve(host = '0.0.0.0', port = 4000, allow_unsafe_werkzeug = True)
