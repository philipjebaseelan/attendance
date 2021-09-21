function validation()
{
    var name = document.forms["form"]["name"];
    var email = document.forms["form"]["email"];
    var username = document.forms["form"]["username"];
    var password = document.forms["form"]["password"];
    var confirm = document.forms["form"]["confirm"];

    let info = [name, email, username, password, confirm]
    let header = ['name', 'email', 'username', 'password', 'confirm']

    let invalid = 0;
    let valid = 0;

    let empty_message = 'Please enter your ';


    for(let i = 0; i < info.length; i++)
    {
        if(info[i].value == '' && header[i] != 'confirm')
        {
            alert(empty_message.concat(header[i]));
            document.getElementById('register-' +header[i]).className += ' error'
            invalid++;
        }

        if(header[i] == 'confirm' && info[i].value == '')
        {
            alert('Please re-enter your password');
            document.getElementById('register-'+header[i]).className += ' error'
            invalid++;
        }

        if(info[i].value != '')
        {
            document.getElementById('register-'+header[i]).className = 'form-control';
            valid++;
        }

    }


    if(invalid > 0)
    {
        return false;
    }
    else if(valid == 5)
    {
        return true;
    }
}
