function register_empty()
{
    var name = document.forms["register-form"]["name"];
    var email = document.forms["register-form"]["email"];
    var username = document.forms["register-form"]["username"];
    var password = document.forms["register-form"]["password"];
    var confirm = document.forms["register-form"]["confirm"];

    let info = [name, email, username, password, confirm]
    let header = ['name', 'email', 'username', 'password', 'confirm']

    let valid = 0;
    let invalid = 0;

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



function register_validate()
{
    var username = document.forms["register-form"]["username"].value;
    var password = document.forms["register-form"]["password"].value;
    var confirm = document.forms["register-form"]["confirm"].value;


    let valid = 0;
    let invalid = 0;

    if(password != confirm)
    {
        alert('The Passwords do not match.');
        document.getElementById('register-password').className += ' error'
        document.getElementById('register-confirm').className += ' error'
        invalid++;
    }





    if(invalid > 0)
    {
        return false;
    }
    else(valid == 3)
    {
        return true;
    }
}




function signin_empty()
{
    var username = document.forms["signin-form"]["username"];
    var password = document.forms["signin-form"]["password"];

    let info = [username, password]
    let header = ['username', 'password']

    let valid = 0;
    let invalid = 0;

    let empty_message = 'Please enter your ';

    for(let i = 0; i < info.length; i++)
    {
        if(info[i].value == '')
        {
            alert(empty_message.concat(header[i]));
            document.getElementById('signin-' +header[i]).className += ' error'
            invalid++;
        }
        if(info[i].value != '')
        {
            document.getElementById('signin-'+header[i]).className = 'form-control';
            valid++;
        }
    }

    if(invalid > 0)
    {
        return false;
    }
    else(valid == 2)
    {
        return true;
    }

}
