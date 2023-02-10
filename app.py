# project url: https://www.github.com/tomzcn/decentral-http

# feature
# # limit the number of accesses
# todo

import aiohttp
import asyncio
from aiohttp import web
import shelve
import time

def db_init(filename):
    with shelve.open(filename) as db:
        if 'server_db' not in db:
            db['server_db']={}
        if 'article' not in db:
            db['article']=''
            
db_init('./server.db')
db_init('./s1.db')
db_init('./s2.db')

async def say(url,message,myfile):
    if await exist(url):
        async with aiohttp.ClientSession() as session:
            async with session.post(url,json=message) as resp:
                print(resp.status)
                data= await resp.json()
        return data
    else:
        file_del_server(myfile,url)
        return {'message':'Url does not exist.'}

async def file_del_server(myfile,server_url):
    with shelve.open(myfile) as db:
        db2=db['server_db']
        del db2[server_url]
        db['server_db']=db2
        return True
    return False

async def file_add_server(myfile,server_url):
    with shelve.open(myfile) as db:
        db2=db['server_db']
        db2[server_url]=1
        db['server_db']=db2
        return True
    return False

async def exist(url):
    message={'message':'What channel?'}
    async with aiohttp.ClientSession() as session:
        async with session.post(url,json=message) as resp:
            print(resp.status)
            json_r=await resp.json()
            r=json_r['message']
            if resp.status == 200 and \
                r=='entrance:test.tomzcn.decentral-http-entrance':
                return True
    return False

def capacity(myfile):
    date=time.strftime('cap_date %Y-%m-%d',time.gmtime(time.time()))
    with shelve.open(myfile) as db:
        if date in db:
            load=db['date']
            load=load+1
            if load > 1000:
                raise()
        else:
            db['date']=1
            load=1
    return load

def capacity_len(article):
    if len(article) > 1000000:
        raise()

async def server_post_template(request,myurl,myfile):
    capacity(myfile)
    req_json=await request.json()
    data={'message':'ok'}
    if req_json['message']=='What channel?':
        data={'message':'entrance:test.tomzcn.decentral-http-entrance'}
    if req_json['message']=='add_server':
        print('=============add_server========================')
        print(myurl)
        server_url=req_json['server_url']
        exist_resp=await exist(server_url)
        print(exist_resp)
        if not exist_resp:
            raise()
        with shelve.open(myfile) as db:
            db1=db['server_db'].copy()
        if server_url not in db1 and exist_resp:
            # Record the server locally
            print('4')
            await file_add_server(myfile,server_url)
            # Tell all servers to add this server
            print('2')
            for i in db1.keys():
                message={'message':'broadcast_add_server','server_url':server_url}
                print(i)
                await say(i,message,myfile)
            # Tell all servers to the new server
            print('1')
            for i in db1.keys():
                message={'message':'broadcast_add_server','server_url':i}
                await say(server_url,message,myfile)
            # Tell the new server to record this server
            print('3')
            message={'message':'broadcast_add_server','server_url':myurl}
            await say(server_url,message,myfile)
    if req_json['message']=='broadcast_add_server':
        print('=============broadcast_add_server==================')
        print(myurl)
        server_url=req_json['server_url']
        with shelve.open(myfile) as db:
            db1=db['server_db'].copy()
            print(myfile)
            print(db1,'db1')
        if server_url not in db1:
            # Record the server locally
            print('4')
            await file_add_server(myfile,server_url)
    if req_json['message']=='read_article':
        print('=============read article==================')
        with shelve.open(myfile) as db:
            data={'message':db['article']}
    if req_json['message']=='broadcast_article':
        print('=============broadcast article==================')
        with shelve.open(myfile) as db:
            db['article']=req_json['article']
    if req_json['message']=='article':
        print('=============article==================')
        capacity_len(req_json['article'])
        with shelve.open(myfile) as db:
            db_server=db['server_db']
            db['article']=req_json['article']
        message={'message':'broadcast_article','article':req_json['article']}
        for i in db_server.keys():
            await say(i,message,myfile)
    return data 

routes = web.RouteTableDef()

@routes.post('/server/post') 
async def server_post(request):
    print('server')
    data=await server_post_template(request,'http://localhost:8881/server/post','./server.db')
    return web.json_response(data)

@routes.get('/test') 
def test(request):
    return web.Response(text='test')

@routes.get('/server/homepage') 
def server_homepage(request):
    html="""
<a href="/server/add-server-view">connect a server</a><br>
<a href="/server/article">article</a>
    """
    return web.Response(body=html,content_type='text/html')

@routes.get('/server/add-server-view') 
def server_add_server_view(request):
    html="""
<form id="formElem">
the server url: <input type="text" name="server_url" value="http://localhost:8881/s1/post"><br>
<input type="submit">
</form>
<a href="/server/homepage">homepage</a>
<div id="output"></div>

<script>
  formElem.onsubmit = async (e) => {
    e.preventDefault();
formData=new FormData(formElem)
let message = {
  message: 'add_server',
  server_url: formData.get('server_url')
};
console.log(message);
fetch_data={
    method: 'POST',
    headers: {'Content-Type': 'application/json;charset=utf-8'},
    body: JSON.stringify(message)
}
console.log(fetch_data);
let response = await fetch('/server/post', fetch_data);
console.log(response);
let result = await response.json();
output.innerHTML=(result.message);
};
</script>
    """
    return web.Response(body=html,content_type='text/html')

@routes.get('/server/article') 
def server_article(request):
    html="""
<form id="formElem">
article:<br>
<textarea name="article" rows=10 cols=30></textarea><br>
<input type="submit">
</form>
<a href="/server/homepage">homepage</a>
<div id="output"></div>

<script>
  read = async () => {
    let message = {message: 'read_article'};
    let response = await fetch('/server/post', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json;charset=utf-8'
    },
        body: JSON.stringify(message)
        });
        let result = await response.json();
        //console.log(result);
        formElem.article.innerHTML=result.message;
  };
  //console.log(read);
  read();
  formElem.onsubmit = async (e) => {
        e.preventDefault();
    formData=new FormData(formElem)
    let message = {
    message: 'article',
    article: formData.get('article')
    };
        let response = await fetch('/server/post', {
        method: 'POST',
    headers: {
        'Content-Type': 'application/json;charset=utf-8'
    },
        body: JSON.stringify(message)
        });
        let result = await response.json();
        output.innerHTML=result.message;
  };
</script>
    """
    return web.Response(body=html,content_type='text/html')

@routes.post('/s1/post') 
async def s1_post(request):
    print('s1')
    data=await server_post_template(request,'http://localhost:8881/s1/post','./s1.db')
    return web.json_response(data)

@routes.get('/s1/article') 
def server_article(request):
    html="""
<form id="formElem">
article:<br>
<textarea name="article" rows=10 cols=30></textarea><br>
<input type="submit">
</form>
<a href="/server/homepage">homepage</a>
<div id="output"></div>

<script>
  read = async () => {
    let message = {message: 'read_article'};
    let response = await fetch('/s1/post', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json;charset=utf-8'
    },
        body: JSON.stringify(message)
        });
        let result = await response.json();
        //console.log(result);
        formElem.article.innerHTML=result.message;
  };
  //console.log(read);
  read();
  formElem.onsubmit = async (e) => {
        e.preventDefault();
    formData=new FormData(formElem)
    let message = {
    message: 'article',
    article: formData.get('article')
    };
        let response = await fetch('/s1/post', {
        method: 'POST',
    headers: {
        'Content-Type': 'application/json;charset=utf-8'
    },
        body: JSON.stringify(message)
        });
        let result = await response.json();
        output.innerHTML=result.message;
  };
</script>
    """
    return web.Response(body=html,content_type='text/html')

@routes.post('/s2/post') 
async def s1_post(request):
    print('s2')
    data=await server_post_template(request,'http://localhost:8881/s2/post','./s2.db')
    return web.json_response(data)
    
app = web.Application()
app.router.add_routes(routes)
web.run_app(app,port='8881',host='0.0.0.0')


