## About
In short, this setup listens for code execution requests, processes and returns the output. To do this it spins up Docker containers in the back-end, all execution takes place within it and the output is returned in a legible format to the front-end which requested it in the first place.

It was born as a result of a project to setup an interactive gallery for examples @ [scikit-image](http://scikit-image.org/), the Image Processing library for Python.

This is live here @ [interactive gallery for scikit-image examples](http://sharky93.github.io/docs/gallery/auto_examples/)

## Getting Started

Docker works on the concept of [images](https://docs.docker.com/terms/image/#base-image-def) and [containers](http://docs.docker.com/terms/container/) and a [Dockerfile](http://docs.docker.com/reference/builder/) is what is usually used to build the image

The [Dockerfile](http://docs.docker.com/reference/builder/) provided with the repository helps one build an [image](https://docs.docker.com/terms/image/#base-image-def) which caters to running code which uses the scikit-image library. Basically installs all the dependencies on top of the base image so that it can run running scikit-image code

### Prerequisites
* [Docker](http://docs.docker.com/installation/)
* [Flask](http://flask.pocoo.org/docs/installation/) - the webserver using which we expose the service
* [docker-py](https://github.com/dotcloud/docker-py) - Python library for interacting with the Docker daemon


### Steps
Get the latest copy on your server
`git clone https://github.com/scikit-image/skimage-docker/`

Build the image - `docker build -t docker-skimage:1.0 .`

This has to be run when present in the root directory of the repository, since the [Dockerfile](http://docs.docker.com/reference/builder/) is present there and that is what this command uses

After a successful build, - `docker images` should list 'docker-skimage'

Start the server - `python start.py`, this also prints the current URL at which it is running.

#### Components
There are some major components which interact for the demo to work properly.

**Edit** - Creates an instance of the [Ace](http://ace.c9.io/) editor and loads it with code. There needs to be a source for this code in picking it up directly from the HTML is not possible. It is very often such a case when the code is highlighted, but in our demo it is possible to parse the `<pre>` content, but we instead pick it up by decoding a `base64` encoded string which is embedded in the page, since this is what we used eventually for the main gallery since the method is more robust

**Run** - Fetches code from the editor and sends it to the server and registers handlers for a successful as well as an error response. On receiving the response, the appropriate message boxes are displayed. If the response contains images, they are inserted after the editor

**Revert** - Replaces the editor with a backup of the code snippet, which is created when the page loads for the first time

Similarly if the code generated something on `STDOUT` or `STDERR`, it is received as part of the response and is inserted appropriately


For **setting up a minimal front-end** start with a basic HTML page with a button for `Run` along with an area for the code to exist and one for the output we've used `<textarea>` and `<div>` in the minimal example. The `body` looks something like this :

Other components namely `Edit` and `Revert` are covered in the spruced up version

```	  
<button type="button" class="editcode">Edit</button>
<textarea>
  code here
</textarea>
<button type="button" class="runcode"> Run </button>

<div id="success-message"></div>
<div id="error-message"></div>
    <i class="icon-info-sign"></i> <u>STDOUT</u>
<pre id="stdout"></pre>
<hr class="stdout-group">
<p class="stderr-group">
    <i class="icon-remove-sign"></i> <u>STDERR</u>
</p>
<pre id="stderr"></pre>
<hr class="stderr-group">
```
[Source](https://github.com/sharky93/sharky93.github.io/blob/master/demo/index_min.html)

We use the jQuery library for certain basic operations, add the following to `head` to include them.
```
<script src="http://code.jquery.com/jquery-latest.js"></script>
<script type="text/javascript" src="./static/demo_min.js"></script>
```
We put all the custom JS needed to make the site function in `demo_min.js` available [here](https://github.com/sharky93/sharky93.github.io/blob/master/demo/static/demo_min.js)


**Run** - define the `runcode` function. It removes all output from previous runs, fetches code from the **textarea** - `getcode()`, converts it to a legible JSON format and sends an AJAX request to the server and defines handlers for the success and failure case.
```
$.ajax({
    type: 'POST',
    // Provide correct Content-Type, so that Flask will know how to process it.
    contentType: 'application/json',
    // Encode your data as JSON.
    data: jcode,
    // This is the type of data you're expecting back from the server.
    dataType: 'json',
    url: 'http://ci.scipy.org:8000/runcode',
    success: function (e) {
        // remove animation, show Run
        $('.loading').hide();
        
        handleoutput(e);
        
        $('#success-message').html("Success: " + e.timestamp + " UTC -5").show();
        code_running = false;
    },
    error: function (jqxhr, text_status, error_thrown) {
        $('.loading').hide();

        error_code = jqxhr.status;
        error_text = jqxhr.statusText;

        var error_message = 
        $('#error-message').html("Code " + error_code + " " + error_text).show();
        code_running = false;
    }
});
```
[Source](https://github.com/sharky93/sharky93.github.io/blob/master/demo/static/demo_min.js#L56)

`handleoutput` - TODO

## Demo

[Here](http://sharky93.github.io/demo/index_min.html) is a very minimalist demo

[Here](http://sharky93.github.io/demo/) is a spruced up version with more features, it uses the `Ace` editor for editing the code, clicking anywhere inside the code snippet region invokes the editor, pressing `Shift+Enter` runs the code, has the function to `Reload` the original code snippet

[Here](https://github.com/sharky93/sharky93.github.io/tree/master/demo) is the code used in the demo

Some explanation about **features** from the spruced up demo

**Edit** - Extracts the `base64` encoded string, decodes and calls the `editcode` function which takes as input the code snippet
```
$('.editcode').bind('click', function () {
  var snippet = encodedcode.html();
  snippet = Base64.decode(snippet);

  $('pre').replaceWith('<div id="editor"></editor>');

  editcode(snippet);
});
```

The `editcode` function initializes the `Ace` editor and loads the snippet inside it, sets the mode as `Python`. We attach a handler to the editor which on `change`, changes the height of the editor making it resizable with content
```
editor = ace.edit("editor");

editor.on('change', function () {
    var doc = editor.getSession().getDocument(),
        // line height varies with zoom level and font size
        // correct way to find height is using the renderer
        line_height = editor.renderer.lineHeight,
        code_height = line_height * doc.getLength() + 'px';
    $('#editor').height(code_height);
    editor.resize();
});

// place cursor at end to prevent entire code being selected
// after using setValue (which is a feature)
editor.setValue(snippet, 1);

// editor.setTheme("ace/theme/monokai");
editor.getSession().setMode("ace/mode/python");
```

Obviously a lot more can be achieved as desired. See the [interactive gallery](http://sharky93.github.io/docs/gallery/auto_examples/) ;)

## Configuration
[config.py](https://github.com/scikit-image/skimage-docker/blob/master/config.py) has a few basic parameters defined which can be used to customize the server setup

