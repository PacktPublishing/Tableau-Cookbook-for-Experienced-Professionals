# Import packages
import tableauserverclient as TSC
import pandas as pd

tableau_auth = TSC.PersonalAccessTokenAuth('tsc','my-pat-secret', site_id='my-site-name')
server = TSC.Server('https://10ax.online.tableau.com', use_server_version=True)

with server.auth.sign_in(tableau_auth):
    # get all workbooks
    all_workbooks_items, workbooks_pagination = server.workbooks.get()

    # Create  a dataframe with the workbook name, id and owner
    workbooks_df = pd.DataFrame(
        {
            'Workbook Name': [workbook.name for workbook in all_workbooks_items],
            'Workbook Id': [workbook.id for workbook in all_workbooks_items],
            'Owner': [workbook.owner_id for workbook in all_workbooks_items]
        }
    )
    print(workbooks_df)

    # Store in a variable the workbook we want to update the owner
    workbook_to_update = all_workbooks_items[10]

    # Get a full list of users and store in a variable the user we want as the new owner
    all_users, users_pagination = server.users.get()
    user_id = ''
    for user in all_users:
        if user.fullname == 'Tableau User':
            user_id = user.id
        else:
            None

    # Update the workbook item and update the workbook in Tableau Cloud
    workbook_to_update.owner_id = user_id
    server.workbooks.update(workbook_to_update)
