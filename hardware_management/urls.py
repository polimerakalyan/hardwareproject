from django.urls import path
from . import views

urlpatterns = [
    path('register/manager/', views.manager_register, name='manager_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/create-employee/', views.create_employee, name='create_employee'),
    path('manager/delete-employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('manager/employee-list/', views.employee_list, name='employee_list'),
    path('manager/create-project/', views.create_project, name='create_project'),
    path('delete-project/<int:project_id>/', views.delete_project, name='delete_project'),
path('export-all-projects/', views.export_all_projects_excel, name='export_all_projects_excel'),

     path('manager/project-assignments/<int:project_id>/', views.project_assignments, name='project_assignments'),
     path('export_project_hardware_excel/<int:project_id>/', views.export_project_hardware_excel,name='export_project_hardware_excel'),
    path('manager/manage-hardware/', views.manage_hardware, name='manage_hardware'),
    path('manager/add-hardware/', views.add_hardware, name='add_hardware'),
      path('download-hardware-template/', views.download_hardware_template, name='download_hardware_template'),
    path('manager/edit-hardware/<int:hardware_id>/', views.edit_hardware, name='edit_hardware'),
    path('manager/delete-hardware/<int:hardware_id>/', views.delete_hardware, name='delete_hardware'),
    path('manager/manage-hardware-types/', views.manage_hardware_types, name='manage_hardware_types'),
    path('manager/create-assignment/', views.create_assignment, name='create_assignment'),
    path('manager/view-assignments/', views.view_assignments, name='view_assignments'),
    path('manager/assignment-details/<int:assignment_id>/', views.assignment_details, name='assignment_details'),
    path('manager/return-assignment/<int:assignment_id>/', views.return_assignment, name='return_assignment'),
     path('manager/serial-entries/', views.view_serial_entries, name='view_serial_entries'),
    path('manager/verify-serial/<int:entry_id>/', views.verify_serial_entry, name='verify_serial_entry'),
    path('manager/verify-all/<int:assignment_id>/', views.verify_all_employee_entries, name='verify_all_employee_entries'),
        path('manager/verification-status/', views.manager_verification_status, name='manager_verification_status'),
            path('manager/verification-details/<int:assignment_id>/', views.manager_verification_details, name='manager_verification_details'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/my-assignments/', views.view_my_assignments, name='view_my_assignments'),
    path('employee/assignment-details/<int:assignment_id>/', views.my_assignment_details, name='my_assignment_details'),
    path('employee/enter-serials/<int:assignment_id>/', views.enter_serial_numbers, name='enter_serial_numbers'),
    path('employee/edit-serials/<int:assignment_id>/', views.edit_serial_numbers, name='edit_serial_numbers'),
    path('employee/my-hardware/', views.my_hardware, name='my_hardware'),
        path('employee/export-my-hardware/', views.export_my_hardware_excel, name='export_my_hardware_excel'),
path('export-assignment/<int:assignment_id>/', views.export_assignment_excel, name='export_assignment_excel'),

    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    
    path('api/hardware-by-type/', views.api_get_hardware_by_type, name='api_hardware_by_type'),
    path('api/assignment/<int:assignment_id>/', views.api_get_assignment_details, name='api_assignment_details'),
    path('api/check-serial/', views.api_check_serial_exists, name='api_check_serial_exists'),
        path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/<uuid:token>/', views.verify_otp, name='verify_otp'),
    path('reset-password/<uuid:token>/', views.reset_password, name='reset_password'),
    path('manager/export-employees-hardware/', views.export_all_employees_hardware, name='export_employees_hardware'),
    path('manager/chatbot-api/', views.chatbot_api, name='chatbot_api'),
    path('manager/chatbot-stats/', views.chatbot_stats_api, name='chatbot_stats_api'),
        path('manager/chatbot/', views.chatbot_view, name='chatbot'),

            path('manager/bulk-create-employees/', views.bulk_create_employees, name='bulk_create_employees'),
    path('manager/download-sample-csv/', views.download_sample_csv, name='download_sample_csv'),






    # Add to urlpatterns
# Employee transfer URLs
path('employee/request-transfer/', views.request_hardware_transfer, name='request_hardware_transfer'),
path('employee/my-transfers/', views.my_transfers, name='my_transfers'),
path('employee/transfer-tracking/<int:transfer_id>/', views.transfer_tracking, name='transfer_tracking'),
path('employee/update-transfer-status/<int:transfer_id>/', views.update_transfer_status_employee, name='update_transfer_status_employee'),

# Manager transfer URLs
path('manager/transfer-requests/', views.manager_transfer_requests, name='manager_transfer_requests'),
path('manager/approve-transfer/<int:transfer_id>/', views.approve_transfer_request, name='approve_transfer_request'),
path('manager/reject-transfer/<int:transfer_id>/', views.reject_transfer_request, name='reject_transfer_request'),
path('manager/transfer_details/<int:transfer_id>/', views.transfer_details, name='transfer_details'),
path('verify-asset-entry/<int:entry_id>/', views.verify_asset_entry, name='verify_asset_entry'),


    
]
