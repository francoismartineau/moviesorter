const sortable = new Sortable.default(document.querySelectorAll('#frames-container'), {
    draggable: '.frame-container', // except if class "right"
    sortAnimation: {
      duration: 200,
      delay: 0,
      easingFunction: 'ease-in-out',
    },
    plugins: [SortAnimation.default],
    mirror: {
        constrainDimensions: true,
    }
});

sortable.on('drag:start', (event) => {
    const currentTarget = event.originalEvent.target;
    if (noDrag(currentTarget)) {
        event.cancel();
    }    
});

function noDrag(currentTarget) {
    return currentTarget.classList.contains('right');
}

/*
const hasClass = (element, classesToPrevent) => {
    let res = false;
    let currentElem = element;
    
    while (currentElem) {
      const currElemHasClass = Array.from(currentElem.classList).some((cls) => classesToPrevent.includes(cls));
      if (currElemHasClass) {
        res = true;
        currentElem = undefined;
      } else {
        currentElem = currentElem.parentElement;
      }
    }

    return res;
  }
  */