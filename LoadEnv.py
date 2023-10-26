
def get_env(key, default='', output=True, In=False):
    def no_read():
        if In:
            return input('请输入sockboom key:')
        if output:
            print(f"未填写环境变量 {key} 请添加")
            exit(0)
        return default

    return environ.get(key) if environ.get(key) else no_read()
