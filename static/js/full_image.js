        // Go back to list_details when image is clicked
        document.querySelector('img').addEventListener('click', function() {
          window.history.back();
      });

      // Go back to list_details when spacebar is pressed
      document.addEventListener('keydown', function(event) {
          if (event.code === 'Space') {
              window.history.back();
          }
      });