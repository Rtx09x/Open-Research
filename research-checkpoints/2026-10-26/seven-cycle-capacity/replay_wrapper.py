import resource,runpy,sys,time,json
resource.setrlimit(resource.RLIMIT_AS,(2048*1024*1024,2048*1024*1024))
resource.setrlimit(resource.RLIMIT_CPU,(280,285))
t=time.monotonic();sys.path.insert(0,'published');sys.argv=['verify_arithmetic.py','--recomputed']
try:runpy.run_path('published/verify_arithmetic.py',run_name='__main__')
finally:open('certificate_resources.json','w').write(json.dumps({'wall_seconds':time.monotonic()-t,'maxrss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
