def split_sentences(text):
    sentences = text.split('.')
    sentences = [i.strip() for i in sentences]
    sentences = [i for i in sentences if len(i) > 0 ]
    return sentences

def template_head(taskid, docid, anid):
    text = ''' 
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    <meta charset="utf-8">
    <html>
      <head>
        <script src="jquery.min.js"></script>
       <title>TASK 1: Process Identification </title>
      </head>
      <body>

        <h1>TASK 1: Process Identification</h1>

        <table border="1">
          <input type="hidden" id="taskid" value="%s" disabled>
          <tr><b>DOC ID: </b> <input type="text" id="docid" value="%s" disabled> </tr> <br>
          <tr><b>YOUR ID: </b> <input type="text" id="anid" value="%s" ></tr>
          <br><br>
      ''' % (taskid, docid, anid)
    return text

#print (template_head('1','2'))

def template_body(sentences):
    idx = 0
    fulltext = ''
    for i in sentences:
        text = '''
    <tr>
        <td width="20px">%d</td>
        <td width="200px">%s</td>
        <td>
          <select id="%s">
            <option value="1" selected="selected">Process</option>
            <option value="0">Non-Process</option>
          </select>
        </td>
      </tr>
      ''' % (idx+1, sentences[idx], idx+1)
        idx += 1
        fulltext = fulltext+' '+text

    foot = '''

    </table>
   
    <button id="DownloadButton">CREATE FILE!</button>
    <div id="generated" style="display:none">
      <a href="#" id="DownloadLink">DOWNLOAD</a>
      <textarea id="ResultXml" style="width: 100%; height: 30em" readonly="readonly"></textarea>
    </div>
    '''

    return fulltext+foot

def js_xml(sentences):
    head = '''
      '<taskid> <?taskid?> </taskid>',
      '<anid> <?anid?> </anid>',
      '<docid> <?docid?> </docid>',
    '''
    idx = 0
    fulltext = ''
    for i in sentences:
        text = '''
        '<s%s><?s%s?></s%s>',''' % (idx+1, idx+1, idx+1)
        idx += 1
        fulltext = fulltext+' '+text
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
    idx = 0
    fulltext = ''
    for i in sentences:
        text = '''
        's%s': $('#%s').val(),''' % (idx+1, idx+1)
        idx += 1
        fulltext = fulltext+' '+text

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

text = "This is sentence one. This is sentence two. This is sentence three. This is sentence four. This is sentence five. This is sentence six."

taskid, anid, docid = '1', 'your name here', 'sample'
fname = docid+'_Task_'+taskid+'.html'
sentences = split_sentences(text)
template = template_head(taskid, docid, anid) + '\n' + template_body(sentences) + '\n' + template_js(taskid, anid, docid, sentences)
with open(fname, 'w') as fw:
    fw.write(template)
