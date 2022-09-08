#templates
land_template = 'land.html'
register_template = 'authenticate/register.html'
login_template = 'authenticate/login.html'
profile_template = 'authenticate/profile.html'
logout_template = 'authenticate/logout.html'
password_change_template = 'authenticate/password_change.html'
password_change_done_template = 'authenticate/password_change_done.html'
book_detail_template = 'managing/book_detail.html'

#urls
land_url = "land"
register_url = "authenticate:user_register"
login_url = "authenticate:user_login"
profile_url = "authenticate:user_profile"
logout_url = "authenticate:user_logout"
password_change_url = "authenticate:user_password_change"
password_change_done_url = "authenticate:user_password_change_done"
