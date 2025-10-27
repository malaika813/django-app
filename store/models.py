from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATE_CHOICES = (
    ('Punjab', 'Punjab'),
    ('Sindh', 'Sindh'),
    ('Khyber Pakhtunkhwa', 'Khyber Pakhtunkhwa'),
    ('Balochistan', 'Balochistan'),
    ('Islamabad Capital Territory', 'Islamabad Capital Territory'),
    ('Azad Jammu and Kashmir', 'Azad Jammu and Kashmir'),
    ('Gilgit-Baltistan', 'Gilgit-Baltistan'),
    ('FATA', 'FATA (Former Federally Administered Tribal Areas)'),
    ('Bahawalpur Division', 'Bahawalpur Division'),
    ('Faisalabad Division', 'Faisalabad Division'),
    ('Gujranwala Division', 'Gujranwala Division'),
    ('Lahore Division', 'Lahore Division'),
    ('Multan Division', 'Multan Division'),
    ('Rawalpindi Division', 'Rawalpindi Division'),
    ('Sargodha Division', 'Sargodha Division'),
    ('Hyderabad Division', 'Hyderabad Division'),
    ('Karachi Division', 'Karachi Division'),
    ('Larkana Division', 'Larkana Division'),
    ('Mirpurkhas Division', 'Mirpurkhas Division'),
    ('Sukkur Division', 'Sukkur Division'),
)


CATEGORY_CHOICES=(
    ('C0','cow-ghee'),#( value: category)
    ('bf','buffalo-ghee'),
    ('ml','Milk'),
    ('mk','MilkShake'),
    ('CR','crud'),
    ('L','Lassi'),
    ('CR','crud'),
    ('CR','Chai'),
    ('Cf','Coffee'),
    
      
)
class product(models.Model):# category model
    product_id=models.AutoField
    title=models.CharField(max_length=100, default="Default Title")
    description=models.TextField()  
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    composition=models.TextField(default='')
    category=models.CharField(choices=CATEGORY_CHOICES ,max_length=2)
    image=models.ImageField(upload_to="images")
    def __str__(self) :
        return self.title



#model adress 
class Customer(models.Model):
    user=models.ForeignKey(User , on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    mobile=models.IntegerField(default=0)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES ,max_length=100)
    
    def __str__(self):
        return self.name
    
    


# cart model
class Cart(models.Model):
    user=models.ForeignKey(User , on_delete=models.CASCADE)
    product=models.ForeignKey(product , on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
    
# orderplaced model
STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)
class OrderPlaced(models.Model):
    user=models.ForeignKey(User , on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer , on_delete=models.CASCADE)
    product=models.ForeignKey(product , on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50 ,choices=STATUS_CHOICES ,default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
    
 