$('#submit-order-button').click(function(){    
    let frame_times = [...document.querySelectorAll('.frame')].map(el => el.id.split("frame-time-")[1]);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
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
            addResultClasses(result.success);
            if (result.success)
            {
                displayFrameTimes();
            }
        }
    })
});

function displayFrameTimes()
{
    let frame_time_displays = document.querySelectorAll('.frame-time-display');
    for (const frame_time_display of frame_time_displays)
    {
        const frame_time = frame_time_display.parentElement.id.split("frame-time-")[1];
        frame_time_display.innerHTML = secondsToHourMinSec(frame_time);
    }
}

function addResultClasses(success)
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
    }
    else
    {
        resultClass = 'alert-danger';
        resultClassRemove = 'alert-success'
        framesClass = 'wrong';
        framesClassRemove = 'right';
    }
    document.getElementById('result').classList.add(resultClass);
    document.getElementById('result').classList.remove(resultClassRemove);
    let frames = document.querySelectorAll('div.frame img');
    for (const f of frames)
    {
        f.classList.add(framesClass);
        f.classList.remove(framesClassRemove);
    }
}

function secondsToHourMinSec(seconds)
{
    return new Date(seconds * 1000).toISOString().substring(11, 19);
}