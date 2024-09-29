// GENERATE SCRIPT
document.getElementById('guideForm').onsubmit = async function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const response = await fetch('/generate_script', {
        method: 'POST',
        body: formData
    });
    const data = await response.json();
    document.getElementById('scriptOutput').innerHTML = data.script;
};



// TEXT TO SPEECH
document.getElementById('voiceForm').onsubmit = async function(event) {
    event.preventDefault()

    const gen_text = document.getElementById('scriptOutput').innerHTML;
    const textinput = gen_text.replace(/(<([^>]+)>)/ig, '')
    console.log(textinput); // Check if this logs the correct text
    
    if (!textinput) {
        alert("Text input is empty.");
        return;
    }
    var lang = document.getElementById('language');
    const langv = lang.value;
    console.log(langv)
    const is_slow = document.querySelector('input[name="slow"]:checked').value;
    console.log(is_slow)

    const response = await fetch("/gen_voice", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: textinput, lang: langv, is_slow: is_slow })
    });

    const data = await response.json();
    console.log(data)
    alert(data.mp3file)

    // document.getElementById('voiceoverAudio').src = data.mp3file;
};


// RECORD VIDEO
document.getElementById('videoForm').onclick = async function(event) {
    event.preventDefault();
    const osType = document.getElementById('osType').value;
    const response = await fetch('/record_screen', {
        method: 'POST',
        body: JSON.stringify({ os_type: osType })
    });
    const data = await response.json();
    document.getElementById('recordingOutput').textContent = `Recording saved as ${data.output_file}`;
};
