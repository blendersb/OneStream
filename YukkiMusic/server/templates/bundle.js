
/**
 * Show user confirmation dialog upon main button click
 */
function onMainButtonClick() {
    //   const selectedDates = AirDatepickerGlobal.selectedDates;
    //   // Iterate throught the selected dates and format them
    //   let msgToShow = `You selected ${selectedDates.length} dates:`;
    //   selectedDates.map((date) => {
    //     const day = date.getDate();
    //     const month = date.getMonth() + 1;
    //     const year = date.getFullYear();
    //     // get time from date and convert it to HH:MM
    //     const time = date.toTimeString().match(/([0-9]{2}:[0-9]{2})/)[1];
    //     // get timezone offset as HH:MM
    //     const offset = date.toString().match(/([-\+][0-9]+)\s/)[1];
    //     // Add these variables to msgToShow
    //     msgToShow += `\n${day}/${month}/${year} ${time} (UTC${offset})`;
    //   });
        const selectedDates = new Date().toString();
      window.Telegram.WebApp.showConfirm("Youselect"+selectedDates, (confirmed) => {
        if (confirmed === true) {
          // HapticFeedback seems to be broken on linux tdesktop at least, it doesn't run the code 
          // after it. So we will just send the data and not run the hapticfeedback
          console.log("before hapticfeedback")
          // window.Telegram.WebApp.HapticFeedback.notificationOccured('success');
          console.log("after hapticfeedback")
          const data = JSON.stringify(selectedDates);
          window.Telegram.WebApp.sendData(data);
        } else {
          window.Telegram.WebApp.HapticFeedback.impactOccurred('light');
        }
      });
    }
    
    
    // function setMainButtonColor(disable=false) {
    //   // Add transparency to the button color
    //   const tgcolor = window.Telegram.WebApp.MainButton.color;
    //   // convert color from hex to rgb
    //   const colorRgb = parseInt(tgcolor.replace('#', ''), 16);
    //   const color = {
    //     r: (colorRgb >> 16) & 255,
    //     g: (colorRgb >> 8) & 255,
    //     b: colorRgb & 255,
    //   };
    
    //   let opacity;
    //   if (disable == true) {
    //     opacity = 0.5;
    //   } else {
    //     opacity = 1;
    //   }
    //   const rgba = `rgba(${color.r}, ${color.g}, ${color.b}, ${opacity})`;
    //   // Telegram currently discards the alpha channel when they convert to hex
    //   // code internally
    //   // so we will manually set the attribute on the button -> doesn't work :(
    //   // window.Telegram.WebApp.MainButton.setParams({'color': hex});
    //   // window.Telegram.WebApp.MainButton.buttonColor = rgba;
    // }
    
    /**
     * Main function. Gets the query params, makes the airdatepicker instance,
     * and expands the webapp if necessary.
    
     */
    function main() {
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.MainButton.show();
        //window.Telegram.WebApp.MainButton.enable();
      //const params = getQueryParams();
    
      //params.then((options) => {
      //  makeAirDatepicker(options);
    
        // Expand the webapp is `timepicker` param and/or `buttons` is passed
        //if ('timepicker' in options || 'buttons' in options) {
          //window.Telegram.WebApp.expand();
        //}
    
        //activateMainButton(AirDatepickerGlobal.selectedDates, options);
      //});
      window.Telegram.WebApp.onEvent('mainButtonClicked', onMainButtonClick);
    }
    
    main();
    