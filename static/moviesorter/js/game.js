const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
var score = 0;

function affectScore(event) {
    switch(event) {
        case 'wrong':
            score -= 5;
            break;
        case 'right':
            const framesQty = [...document.querySelectorAll('.frame-container')].length;
            score += framesQty * 10;
            break;
        }
        document.getElementById('score').innerHTML = score;
}


$( document ).ready(function() {
    requestFrames();
    affectScore();
});

$('#submit-order-button').click(() => {    
    let frame_times = [...document.querySelectorAll('.frame-container')].map(el => el.dataset.time);
    $.ajax(
    {
        type:"POST",                                 
        url: "/submit-order",     
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin', // Do not send CSRF token to another domain.                          
        data:{
            'frame_times[]': frame_times                      
        },
        success: function( result )                   
        {
            $('#result').text(result.text);
            applyResultClasses(result.success);
            if (result.success)
            {
                displayFrameTimes();
                requestFrames();
                affectScore('right');
            }
            else
            {
                affectScore('wrong');
            }
        }
    })
});

function displayFrameTimes()
{
    let frame_time_displays = document.querySelectorAll('.frame-time-display');
    for (const frame_time_display of frame_time_displays)
    {
        const frame_time = frame_time_display.parentElement.dataset.time;
        frame_time_display.innerHTML = secondsToHourMinSec(frame_time);
    }
}
function secondsToHourMinSec(seconds)
{
    return new Date(seconds * 1000).toISOString().substring(11, 19);
}

function applyResultClasses(success)
{
    var resultClass = '';
    var resultClassRemove = '';
    var framesClass = '';
    var framesClassRemove = '';
    if (success)
    {
        resultClass = 'alert-success';
        resultClassRemove = 'alert-danger';
        framesClass = 'right';
        framesClassRemove = 'wrong';
        let frames = document.querySelectorAll('div.frame-container img');
        for (const f of frames)
        {
            f.classList.add(framesClass);
            f.classList.remove(framesClassRemove);
        }        
    }
    else
    {
        resultClass = 'alert-danger';
        resultClassRemove = 'alert-success'
    }
    document.getElementById('result').classList.add(resultClass);
    document.getElementById('result').classList.remove(resultClassRemove);

}

function requestFrames() {
    const framesContainer = document.getElementById('frames-container');
    const movieTitle = framesContainer.getAttribute('data-movie-title');
    const exceptCloudinaryIds = Array.from(framesContainer.children).map((el) => { return el.dataset.cloudinaryId });

    $.ajax(
        {
            type:"POST",                                 
            url: "/request-frames",     
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin',                         
            data:{
                'movie-title': movieTitle,
                'except-cloudinary-ids[]': exceptCloudinaryIds                      
            },
            success: function( result )                   
            {
                insertFrames(framesContainer, result.frames);
            }
        })
}

function insertFrames(framesContainer, frames) {
    for (const frame of frames) {
        var img = document.createElement('img');
        img.src = frame.url;

        var label = document.createElement('label');
        label.classList.add('frame-time-display');

        var frameContainer = document.createElement('div');
        frameContainer.classList.add('frame-container');
        frameContainer.dataset.time = frame.time;
        frameContainer.dataset.cloudinaryId = frame.cloudinaryId;
        frameContainer.appendChild(img);
        frameContainer.appendChild(label);
        if (frameW)
            frameContainer.style.width = frameW+'em';

        framesContainer.append(frameContainer);
    }
}

// ----------------------------------------
var frameW;
function setFrameSize(event) {
    const frameContainers = document.querySelectorAll('div.frame-container');
    const val = event.target.value / 1000;
    const w = 10 + Math.floor(Math.pow(30, val));
    frameW = w;
    for (const frameContainer of frameContainers) {
        frameContainer.style.width = w+'em';
    }
}