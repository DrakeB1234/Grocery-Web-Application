module.exports = {
    checkUsername: function(x) {
        // only allows a-Z0-9_- and 4-20 characters
        const regex = /^[\w-]{4,20}$/; 
        if(regex.test(x)){
            return true;
        }
        return false;
    },
    checkEmail: function(x) {
        const regex = /^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
        if(regex.test(x)){
            return true;
        }
        return false;
    },
    checkPassword: function(x) {
        // checks no spaces and between 5-200 characters
        const regex = /^[^\s]{5,200}$/;
        if(regex.test(x)){
            return true;
        }
        return false;
    },
}