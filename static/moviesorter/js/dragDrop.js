const sortable = new Sortable.default(document.querySelectorAll('.frame-container-container'), {
    draggable: '.frame-container',
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



/*
document.addEventListener('DOMContentLoaded', (_) => {

    var draggedEl = null;
    function handleDragStart(e) {
        this.style.opacity = '0.4';
        
        draggedEl = this;
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/html', this.innerHTML);      
    }
  
    function handleDragOver(e) {
        if (e.preventDefault) {
            e.preventDefault();             // Sans, la souris deviendrait un symbol d'interdit.
        }
        e.dataTransfer.dropEffect = 'move';
        return false;
    }
  
    function handleDragEnter(_) {
        this.classList.add('over');
    }
  
    function handleDragLeave(_) {
        this.classList.remove('over');
    }

    function handleDrop(e) {
        if (e.stopPropagation) {
            e.stopPropagation();            // stops the browser from redirecting.
        }

        if (draggedEl != this) {
            draggedEl.innerHTML = this.innerHTML;
            this.innerHTML = e.dataTransfer.getData('text/html');
        }  
              
        return false;
    }

    function handleDragEnd(_) {
        this.style.opacity = '1';
    
        items.forEach(function (item) {
          item.classList.remove('over');
        });
    }
  
    let items = document.querySelectorAll('.frame-container');
    items.forEach(function(item) {
      item.addEventListener('dragstart', handleDragStart);
      item.addEventListener('dragover', handleDragOver);
      item.addEventListener('dragenter', handleDragEnter);
      item.addEventListener('dragleave', handleDragLeave);
      item.addEventListener('dragend', handleDragEnd);
      item.addEventListener('drop', handleDrop);
    });
  });
  */