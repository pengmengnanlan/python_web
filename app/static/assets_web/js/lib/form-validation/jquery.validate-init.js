var form_validation = function() {
    var e = function() {
            jQuery(".form-valide").validate({
                ignore: [],
                errorClass: "invalid-feedback animated fadeInDown",
                errorElement: "div",
                errorPlacement: function(e, a) {
                    jQuery(a).parents(".form-group > div").append(e)
                },
                highlight: function(e) {
                    jQuery(e).closest(".form-group").removeClass("is-invalid").addClass("is-invalid")
                },
                success: function(e) {
                    jQuery(e).closest(".form-group").removeClass("is-invalid"), jQuery(e).remove()
                },
                rules: {
                    "val-login-name": {
                        required: !0,
                        minlength: 1
                    },
                    "val-login-pwd": {
                        required: !0,
                        minlength: 1
                    },
                    "val-username": {
                        required: !0,
                        minlength: 3
                    },
                    "val-email": {
                        required: !0,
                        email: !0
                    },
                    "val-password": {
                        required: !0,
                        minlength: 5
                    },
                    "val-confirm-password": {
                        required: !0,
                        equalTo: "#val-password"
                    },
                    "val-select2": {
                        required: !0
                    },
                    "val-select2-multiple": {
                        required: !0,
                        minlength: 2
                    },
                    "val-suggestions": {
                        required: !0,
                        minlength: 5
                    },
                    "val-mac": {
                        required: !0,
                        minlength: 5
                    },
                    "val-model":{
                        required: !0,
                        minlength: 3
                    },
                    "val-group":{
                        required: !0,
                        minlength: 1
                    },
                    "val-key":{
                        required: !0,
                        minlength: 5
                    },
                    "val-skill": {
                        required: !0
                    },
                    "val-currency": {
                        required: !0,
                        currency: ["$", !0]
                    },
                    "val-website": {
                        required: !0,
                        url: !0
                    },
                    "val-phoneus": {
                        required: !0,
                        phoneUS: !0
                    },
                    "val-digits": {
                        required: !0,
                        digits: !0
                    },
                    "val-number": {
                        required: !0,
                        number: !0
                    },
                    "val-range": {
                        required: !0,
                        range: [1, 5]
                    },
                    "val-terms": {
                        required: !0
                    }
                },
                messages: {
                    "val-login-name": {
                        required: "请输入用户名！"
                    },
                    "val-login-pwd": {
                        required: "请输入密码！"
                    },
                    "val-username": {
                        required: "请输入用户名！",
                        minlength: "用户名必须包含3个字符！"
                    },
                    "val-email": "Please enter a valid email address",
                    "val-password": {
                        required: "请提供一个可靠密码！",
                        minlength: "密码长度必须大于5位数！"
                    },
                    "val-confirm-password": {
                        required: "请再次确认您的密码！",
                        minlength: "密码长度必须大于5位数！",
                        equalTo: "请输入和上面一样的密码！"
                    },
                    "val-select2": "Please select a value!",
                    "val-select2-multiple": "Please select at least 2 values!",
                    "val-suggestions": "please enter something",
                    "val-mac": "请输入正确的物理地址！",
                    "val-model":"请输入正确的终端模型！",
                    "val-key":"请输入正确的密钥！",
                    "val-group":"请输入分组名称",
                    "val-skill": "Please select a skill!",
                    "val-currency": "Please enter a price!",
                    "val-website": "Please enter your website!",
                    "val-phoneus": "Please enter a US phone!",
                    "val-digits": "Please enter only digits!",
                    "val-number": "Please enter a number!",
                    "val-range": "Please enter a number between 1 and 5!",
                    "val-terms": "You must agree to the service terms!"
                }
            })
        }
    return {
        init: function() {
            e(), a(), jQuery(".js-select2").on("change", function() {
                jQuery(this).valid()
            })
        }
    }
}();
jQuery(function() {
    form_validation.init()
});