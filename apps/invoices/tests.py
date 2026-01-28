from django.test import TestCase
from django.contrib.auth.models import User
from apps.clients.models import Client
from apps.products.models import Product, Category
from .models import Invoice, InvoiceItem

class InvoiceModelTest(TestCase):
    def setUp(self):
        # Crear datos de prueba
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            price=100.00,
            stock=10,
            sku="TEST123"
        )
        self.client = Client.objects.create(
            name="Test Client",
            email="test@client.com",
            client_type="individual"
        )
    
    def test_create_invoice(self):
        """Test crear una factura"""
        invoice = Invoice.objects.create(
            client=self.client,
            invoice_date="2024-01-01",
            due_date="2024-01-15",
            total=100.00
        )
        self.assertEqual(invoice.client.name, "Test Client")
        self.assertEqual(str(invoice), f"Factura {invoice.invoice_number} - Test Client")
