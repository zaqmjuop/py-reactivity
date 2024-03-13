import weakref
WeakSet = weakref.WeakSet
if __name__ == '__main__':
  class MyClass:
      pass

  ws = weakref.WeakSet()
  o = MyClass()
  ws.add(o)

  print(len(ws))  # 输出：1

  del o  # 删除o的唯一非弱引用

  # 等待垃圾收集器运行
  import gc
  gc.collect()

  print(len(ws))  # 输出：0