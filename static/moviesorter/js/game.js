const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
var score = 0;


$( document ).ready(function() {
    requestFrames();
    initScore();
});

function requestFrames() {
    const framesContainer = document.getElementById('frames-container');
    const movieTitle = getMovieTitle(); 
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

function initScore() {
    score = 0;
    document.getElementById('score').innerHTML = score;
    const movieTitle = getMovieTitle(); 
    console.log(movieTitle);
    var bestScore;
    $.ajax(
    {
        type:"POST",                                 
        url: "/request-best-score",     
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin', // Do not send CSRF token to another domain.                          
        data:{
            'movie_title': movieTitle,
        },
        success: function( result )                   
        {
            bestScore = result.bestScore;
            document.getElementById('best-score').innerHTML = bestScore;
        }
    })
}

// ----------------------------------------
function submitOrder() {
    const movieTitle = getMovieTitle(); 
    let frame_times = [...document.querySelectorAll('.frame-container')].map(el => el.dataset.time);
    $.ajax(
    {
        type:"POST",                                 
        url: "/submit-order",     
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin', // Do not send CSRF token to another domain.                          
        data:{
            'movie_title': movieTitle,
            'frame_times[]': frame_times,
            'score': score,
        },
        success: function( result )                   
        {
            $('#result').text(result.text);
            applyResultClasses(result.success);
            if (result.success)
            {
                displayFrameTimes();
                requestFrames();
            }
            affectScore(result);
        }
    })
}

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

function affectScore(result) {
    score = result.score;
    document.getElementById('score').innerHTML = score;
    const bestScore = result.bestScore;
    document.getElementById('best-score').innerHTML = bestScore;
}


// ----------------------------------------
function getMovieTitle() {
    const movieTitle = document.getElementById('frames-container').getAttribute('data-movie-title');
    return movieTitle;
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