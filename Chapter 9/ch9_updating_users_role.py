# Import packages
import tableauserverclient as TSC

tableau_auth = TSC.PersonalAccessTokenAuth('my-token-name','my-token-secret', site_id='my-site-name')
server = TSC.Server('https://10ax.online.tableau.com', use_server_version=True)

with server.auth.sign_in(tableau_auth):
    all_users, users_pagination = server.users.get()
    print([user.id for user in all_users])
    print([user.name for user in all_users])
    print([user.site_role for user in all_users])
    #user = all_users[1].id
    #print(user)
    user_id = ''
    for user in all_users:
        if user.fullname == 'Tableau User':
            user_id=user.id
        else:
            None
    print('The user ID: '+ user_id)

    target_user = server.users.get_by_id(user_id)
    target_user.site_role = 'Explorer'
    server.users.update(target_user)
