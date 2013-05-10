var event;
var attendQuery;



function clickedOp(device_id, op)
{
    $.ajax({url:'/remotes/' + device_id + '/clicked/' + op});
}

function dimBedroomLights() 
{
    $.ajax({url:'/actions/dim-bedroom-lights'});
}

function fullPowerBedroomLights() 
{
    $.ajax({url:'/actions/fullpower-bedroom-lights'});
}

