from clean import cleantext
import glob, os

def split_sentences(text):
    sentences = text.split('.')
    sentences = [i.strip() for i in sentences]
    sentences = [i for i in sentences if len(i) > 0 ]
    return sentences

def template_head(taskid, docid, anid, fname):
    text = ''' 
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    <meta charset="utf-8">
    <html>
      <head>
        <script src="jquery.min.js"></script>
       <title>TASK 2: Relation Classification </title>
      </head>
      <body>

        <h1>TASK 2: Relation Classification</h1>

        <table border="1">
          <input type="hidden" id="taskid" value="%s" disabled>
          <tr><b>DOC ID: </b> <input type="text" id="docid" value="%s" disabled> </tr> <br>
          <tr><b>YOUR ID: </b> <input type="text" id="anid" value="%s" ></tr><br>
          <tr><b>TITLE: </b> %s </tr> <br>
          <br>
      ''' % (taskid, docid, anid, fname)
    return text

#print (template_head('1','2'))

def template_body1(sentences):
    head = '''<tr>
        <td width="400px">SENTENCE ID</td>
    '''
    idx = 0
    fulltext = ''
    for i in sentences:
        text = '''<td>%s</td> 
      ''' % (idx+1)
        idx += 1
        fulltext = fulltext+' '+text

    return head+fulltext+'</tr>'

def template_body2(sentences):
    fulltext = ''
    for i in range(len(sentences)): #+1
        a = '<td>%s.) %s</td>' % (i+1, sentences[i])
        
        bid = 1
        btext = ''
        for j in range(i+1):
            if i+1 == bid:
                #b = '<td>s_%s_%s</td>\n' % (i+1, bid)
                b = '<td></td>\n'
            else:
                b = '''
                <td> <div><span title="%s">(%s)</span> <span title="%s">(%s)</span></div>
                    <select id="s_%s_%s">
                    <option value="5" selected="selected">none</option>
                    <option value="1">sequence_of</option>
                    <option value="2">subprocess_of</option>
                    <option value="3">conditional_of</option>
                    <option value="4">detail_of</option>
                    </select>
                </td> 
                ''' % (sentences[i],i+1, sentences[bid-1],bid, i+1, bid)
            bid +=1
            btext = btext+' '+b

        cid = bid
        ctext = ''
        for h in range(len(sentences)-j-1):
            #c = '<td>s_%s_%s</td>\n' % (i+1, cid)
            c = '<td></td>\n'
            cid +=1
            ctext = ctext+' '+c
        
        text = '<tr>'+a+'\n'+btext+'\n'+ctext+'</tr>'
        fulltext = fulltext+text

    
    foot = '''

    </table>
   
    <button id="DownloadButton">CREATE FILE!</button>
    <div id="generated" style="display:none">
      <a href="#" id="DownloadLink">DOWNLOAD</a>
      <textarea id="ResultXml" style="width: 100%; height: 30em" readonly="readonly"></textarea>
    </div>
    '''
    return '<tr>'+fulltext+'</tr>'+foot

def js_xml(sentences):
    head = '''
      '<taskid> <?taskid?> </taskid>',
      '<anid> <?anid?> </anid>',
      '<docid> <?docid?> </docid>',
    '''

    fulltext = ''
    for i in range(len(sentences)):
        bid = 1
        btext = ''
        for j in range(i+1):
            if i+1 == bid:
                b = ''
            else:
                b = '''
                '<s_%s_%s><?s_%s_%s?></s_%s_%s>',''' % (i+1, bid, i+1, bid, i+1, bid)
            bid +=1
            btext = btext+' '+b
        fulltext = fulltext+btext

    foot = '''
    '</annotation_task_1>'
    ].join('\\r\\n');
    '''
    return head+fulltext+foot

def js_func(sentences):
    head = '''
    function update() {
      var variables = {
      'taskid': $('#taskid').val(),
      'anid': $('#anid').val(),
      'docid': $('#docid').val(),'''

    fulltext = ''
    for i in range(len(sentences)):
        bid = 1
        btext = ''
        for j in range(i+1):
            if i+1 == bid:
                b = ''
            else:
                b = '''
                's_%s_%s': $('#s_%s_%s').val(),
                ''' % (i+1, bid, i+1, bid)
                if bid == (len(sentences)-1):
                    b = '''
                    's_%s_%s': $('#s_%s_%s').val()
                    ''' % (i+1, bid, i+1, bid)
                
            bid +=1
            btext = btext+' '+b
        fulltext = fulltext+btext

    return head+fulltext+'};'

def template_js(taskid, anid, docid, sentences):
    head = '''
    <script id="jsbin-javascript">
    $(function () {
    $('#DownloadButton').click(update);
    });

    var template = [
        '<?xml version="1.0"?>',
        '<annotation_task_1>',
    '''
    body = js_xml(sentences)+'\n'+js_func(sentences)+'\n'

    foot = '''
    var newXml = template.replace(/<\?(\w+)\?>/g,
    function(match, name) {
      return variables[name];
    });

    var xmlname = $('#taskid').val()+'_'+$('#anid').val()+'_'+$('#docid').val()+'.xml';
  
    $('#ResultXml').val(newXml);
    $('#DownloadLink')
        .attr('href', 'data:text/xml;base64,' + btoa(newXml))
        .attr('download', xmlname);
    $('#generated').show();
    }

    </script>
    </body>
    </html> '''

    return head+body+foot

# text = "This is sentence one. This is sentence two. This is sentence three. This is sentence four. This is sentence five. This is sentence six."
# #text = "This is sentence one. This is sentence two. This is sentence three."

# taskid, anid, docid = '2', 'your name here', 'sample'
# fname = 'results/'+docid+'_Task_'+taskid+'.html'
# sentences = split_sentences(text)
# txt = '2012up/高流動性・高延性ポリプロピレンの構造と物性 - Copy.txt'
# #sentences = cleantext(txt)

# template = template_head(taskid, docid, anid) + '\n' + template_body1(sentences) + '\n' + template_body2(sentences) + '\n' + template_js(taskid, anid, docid, sentences)
# with open(fname, 'w') as fw:
#     fw.write(template)

def read():
    text = "This is sentence one. This is sentence two. This is sentence three. This is sentence four. This is sentence five."
    taskid, anid, docid, fname = '2', 'your name here', 'sample', 'The title of the document'
    saveresult = 'results/'+docid+'_Task'+taskid+'.html'
    sentences = split_sentences(text)
    template = template_head(taskid, docid, anid, fname) + '\n' + template_body1(sentences) + '\n' + template_body2(sentences) + '\n' + template_js(taskid, anid, docid, sentences)
    with open(saveresult, 'w') as fw:
        fw.write(template)
    print (docid, len(sentences))

def read_all(flder):
    alltxt = glob.glob(flder+"/*.txt")
    i = 87
    for fl in alltxt:
        fname = os.path.basename(fl).split('/')[0][:-4].replace(' ','')
        docid = 'D00'+str(i)
        sentences = cleantext(fl)
        taskid, anid, docid = '2', 'your name here', docid
        saveresult = 'results/2012up/'+docid+'_Task'+taskid+'.html'
        
        template = template_head(taskid, docid, anid, fname) + '\n' + template_body1(sentences) + '\n' + template_body2(sentences) + '\n' + template_js(taskid, anid, docid, sentences)
        with open(saveresult, 'w') as fw:
            fw.write(template)
        print (i, docid, len(sentences))
        i+=1

#read_all("2012up")
read()
