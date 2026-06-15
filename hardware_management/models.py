from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    is_first_login = models.BooleanField(default=True)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_employees')
    phone = models.CharField(max_length=15, blank=True, null=True)
    branch_location = models.CharField(max_length=200, blank=True, null=True)  



    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Project(models.Model):
    project_id = models.CharField(max_length=50, unique=True)
    project_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=200)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.project_id} - {self.project_name}"

class HardwareType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Hardware(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
    )
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='HardwareType',default='1')
    hardware_type = models.ForeignKey(HardwareType, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=100, unique=True)
    model_name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True, null=True)
    specifications = models.TextField(blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    asset_number = models.CharField(max_length=100, unique=True, null=True, blank=True, help_text="Unique asset tag number")


    
    def __str__(self):
        return f"{self.hardware_type.name} - {self.serial_number}"

class HardwareAssignment(models.Model):
    assignment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='hardware_assignments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='hardware_assignments')
    hardware_items = models.ManyToManyField(Hardware, through='HardwareAssignmentItem')
    exam_city = models.CharField(max_length=200, blank=True, null=True, help_text="City where the employee will take the exam")
    assigned_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assignments_made')
    assigned_date = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Assignment {self.assignment_id} - {self.employee.username}"

class HardwareAssignmentItem(models.Model):
    assignment = models.ForeignKey(HardwareAssignment, on_delete=models.CASCADE)
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    condition_at_assignment = models.TextField(blank=True, null=True)
    condition_at_return = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('assignment', 'hardware')

class HardwareSerialEntry(models.Model):
    assignment_item = models.OneToOneField(HardwareAssignmentItem, on_delete=models.CASCADE, related_name='serial_entry')
    serial_number = models.CharField(max_length=100)
    entered_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    entered_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_entries')
    verified_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Serial: {self.serial_number}"
    

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid
import random

User = get_user_model()

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return f"OTP for {self.user.username}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    @classmethod
    def generate_otp(cls, user):
        otp = str(random.randint(100000, 999999))
        expires_at = timezone.now() + timezone.timedelta(seconds=300)  
        
        cls.objects.filter(user=user, is_used=False).update(is_used=True)
        
        return cls.objects.create(
            user=user,
            otp=otp,
            expires_at=expires_at
        )
    
    class Meta:
        ordering = ['-created_at']    

class EmployeeHardwareTransfer(models.Model):
    """Model to track hardware transfer between employees"""
    
    STATUS_CHOICES = (
        ('requested', 'Transfer Requested'),
        ('approved_by_manager', 'Approved by Manager'),
        ('in_transit', 'In Transit'),
        ('received_by_receiver', 'Received by Receiver'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )
    
    TRANSFER_TYPE_CHOICES = (
        ('temporary', 'Temporary Transfer'),
        ('permanent', 'Permanent Transfer'),
    )
    
    transfer_id = models.CharField(max_length=20, unique=True, editable=False)
    
    hardware_items = models.ManyToManyField(Hardware, through='TransferItem', related_name='employee_transfers')
    
    from_employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transfers_given')
    to_employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transfers_received')
    
    from_exam_city = models.CharField(max_length=200)
    to_exam_city = models.CharField(max_length=200)
    from_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name='transfers_from_emp')
    to_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name='transfers_to_emp')
    
    transfer_type = models.CharField(max_length=20, choices=TRANSFER_TYPE_CHOICES, default='temporary')
    reason = models.TextField()
    expected_return_date = models.DateField(null=True, blank=True)
    
    requested_date = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    transfer_date = models.DateField(null=True, blank=True)
    expected_arrival_date = models.DateField()
    actual_arrival_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='transfers_approved_emp')
    
    delivery_method = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    
    requester_notes = models.TextField(blank=True, null=True)
    manager_notes = models.TextField(blank=True, null=True)
    completion_notes = models.TextField(blank=True, null=True)
    
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transfers_created_emp')
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.transfer_id:
            import random
            import string
            date_str = timezone.now().strftime('%Y%m%d')
            random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            self.transfer_id = f"EMP-{date_str}-{random_str}"
        super().save(*args, **kwargs)
    
    @property
    def total_items(self):
        return self.transfer_items.count()
    
    @property
    def received_items_count(self):
        return self.transfer_items.filter(status='received').count()
    
    def __str__(self):
        return f"{self.transfer_id} - {self.total_items} item(s)"


class TransferItem(models.Model):
    """Individual hardware items in a transfer"""
    
    ITEM_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('received', 'Received'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled'),
    )
    
    transfer = models.ForeignKey(EmployeeHardwareTransfer, on_delete=models.CASCADE, related_name='transfer_items')
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=20, choices=ITEM_STATUS_CHOICES, default='pending')
    
    condition_before = models.TextField(blank=True, null=True)
    condition_after = models.TextField(blank=True, null=True)
    
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    
    transfer_date = models.DateField(null=True, blank=True)
    received_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('transfer', 'hardware')
    
    def __str__(self):
        return f"{self.transfer.transfer_id} - {self.hardware.serial_number}"


class TransferHistory(models.Model):
    """Model to track transfer history and updates"""
    transfer = models.ForeignKey(EmployeeHardwareTransfer, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=100, default='action')
    status = models.CharField(max_length=20, choices=EmployeeHardwareTransfer.STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transfer.transfer_id} - {self.action} at {self.created_at}"


class TransferNotification(models.Model):
    """Model to track transfer notifications"""
    transfer = models.ForeignKey(EmployeeHardwareTransfer, on_delete=models.CASCADE, related_name='notifications')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Notification for {self.transfer.transfer_id}"
    


class ChatbotConversation(models.Model):
    """Store chatbot conversations"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chat_conversations')
    message = models.TextField()
    response = models.TextField()
    intent = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at}"


class HardwareKnowledgeBase(models.Model):
    """Knowledge base for AI training"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100, choices=[
        ('hardware', 'Hardware Info'),
        ('procedure', 'Procedure'),
        ('faq', 'FAQ'),
        ('policy', 'Policy'),
    ], default='hardware')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
