// GENERATE SCRIPT
document.getElementById('guideForm').onsubmit = async function(event) {
    event.preventDefault();
    var lang = document.getElementById('scriptlanguage').value;
    var software_name = document.getElementById('software_name').value;
    var os_type = document.getElementById('scriptosType').value;
    console.log(lang, software_name, os_type);

    try {
        const response = await fetch('/generate_script', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ software_name: software_name, lang: lang, os_type: os_type })
        });

        if (response.ok) {
            const data = await response.json(); // Ensure 'data' is defined here
            // Check if the script exists in the response
            if (data.script) {
                document.getElementById('scriptOutput').innerHTML = data.script; // Display the script
            } else {
                document.getElementById('scriptOutput').innerHTML = "No script generated.";
            }
        } else {
            const errorData = await response.json(); // Define errorData here
            alert(`Error: ${errorData.error}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert("Something went wrong: " + error.message);
    }
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
    var lang = document.getElementById('voicelanguage');
    const langv = lang.value;
    console.log(langv)
    const is_slow = document.querySelector('input[name="slow"]:checked').value;
    console.log(is_slow)

    const response = await fetch("/gen_voice", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: textinput, langv: langv, is_slow: is_slow })
    });

    const data = await response.json();
    console.log(data)
    alert(data.mp3file)

    // document.getElementById('voiceoverAudio').src = data.mp3file;
};


// RECORD VIDEO

document.getElementById('videoForm').onsubmit = async function(event) {
    event.preventDefault();

    const os_type = document.getElementById('videoosType').value;

    try {
        const response = await fetch('/record_screen', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',  // Set the content type to JSON
            },
            body: JSON.stringify({ os_type: os_type }),  // Send JSON data
        });

        if (response.ok) {
            const data = await response.json();
            alert(`Recording saved as ${data.output_file}`);
            document.getElementById('recordingOutput').textContent = `Recording saved as ${data.output_file}`;
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.error}`);
            document.getElementById('recordingOutput').textContent = "Recording failed.";
        }
    } catch (error) {
        console.error('Error:', error);
        alert("Something went wrong.");
    }
};
