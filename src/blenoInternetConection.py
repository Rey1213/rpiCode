bleno = require('bleno');
exec = require('child_process').exec;

CHUNK_SIZE = 20;

Descriptor = bleno.Descriptor;

deviceName = 'RaspberrPi3';
myId = '4afb720a-5214-4337-841b-d5f954214877';
data = new Buffer('Send me some data to display');
output = "";
updateCallback;

terminalCallback;
terminalResponse;

START_CHAR = String.fromCharCode(002); //START OF TEXT CHAR
END_CHAR = String.fromCharCode(003);   //END OF TEXT CHAR

function sliceUpResponse(callback, responseText) {
  if (!responseText || !responseText.trim()) return;
  callback(new Buffer(START_CHAR));
  while(responseText !== '') {
      callback(new Buffer(responseText.substring(0, CHUNK_SIZE)));
      responseText = responseText.substring(CHUNK_SIZE);
  }
  callback(new Buffer(END_CHAR));
}

terminal = new bleno.Characteristic({
    uuid : '8bacc104-15eb-4b37-bea6-0df3ac364199',
    properties : ['write','read','notify'],
    onReadRequest : function(offset, callback) {
        console.log("Read request");
        callback(bleno.Characteristic.RESULT_SUCCESS, new Buffer(terminalResponse).slice(offset));
    },
    onWriteRequest : function(newData, offset, withoutResponse, callback) {
        if(offset) {
            callback(bleno.Characteristic.RESULT_ATTR_NOT_LONG);
        } else {
            data = newData.toString('utf8');
            console.log("Command received: [" + data + "]");
            dir = exec(data, function(err, stdout, stderr) {
                if (err) {
                    stringError = JSON.stringify(err);
                    console.log(stringError);
                    callback(bleno.Characteristic.RESULT_SUCCESS);
                    terminalResponse = stringError;
                } else {
                    console.log(stdout);
                    callback(bleno.Characteristic.RESULT_SUCCESS);
                    terminalResponse = stdout;
                }
                if (terminalCallback) sliceUpResponse(terminalCallback, terminalResponse);
            });
        }
    },
    onSubscribe: function(maxValueSize, updateValueCallback) {
       console.log("onSubscribe called");
       terminalCallback = updateValueCallback;
    },
    onUnsubscribe: function() {
        terminalCallback = null;
        console.log("onUnsubscribe");
    }
});

bleno.on('stateChange', function(state) {
    console.log('on -> stateChange: ' + state);
    if (state === 'poweredOn') {
        bleno.startAdvertising(deviceName,[myId]);
    } else {
        bleno.stopAdvertising();
    }
});

bleno.on('advertisingStart', function(error) {
    console.log('on -> advertisingStart: ' + (error ? 'error ' + error : 'success'));
    if (!error) {
        bleno.setServices([
            new bleno.PrimaryService({
                uuid : myId,
                characteristics : [
                    // add characteristics here
                    terminal
                ]
            })
        ]);
        console.log('service added');
    }
});

bleno.on('accept', function(clientAddress) {
    console.log("Accepted connection from: " + clientAddress);
});

bleno.on('disconnect', function(clientAddress) {
    console.log("Disconnected from: " + clientAddress);