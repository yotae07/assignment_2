from django.db import migrations, models
import django.db.models.deletion


def set_initial_product_data(apps, schema_editor):
    Menu = apps.get_model("products", "Menu")
    db_alias = schema_editor.connection.alias
    Menu.objects.using(db_alias).bulk_create([
        Menu(category="salad", name="깔라마리 달래 샐러드", description="해산물 샐러드", isSold=False, badge="new"),
        Menu(category="salad", name="연어 샐러드", description="샐러드", isSold=False, badge="new"),
        Menu(category="salad", name="차돌박이 샐러드", description="샐러드", isSold=False, badge="old"),
        Menu(category="salad", name="닭가슴살 샐러드", description="샐러드", isSold=False, badge="old"),
        Menu(category="milk", name="우유", description="우유", isSold=False, badge="new"),
        Menu(category="milk", name="저지방 우유", description="우유", isSold=False, badge="old"),
        Menu(category="milk", name="고단백 우유", description="우유", isSold=False, badge="old"),
        Menu(category="egg", name="계란", description="계란", isSold=False, badge="new"),
        Menu(category="egg", name="훈제란", description="계란", isSold=False, badge="new"),
        Menu(category="egg", name="메츄리알", description="계란", isSold=True, badge="old"),
        Menu(category="egg", name="무정란", description="계란", isSold=True, badge="old"),
    ])
    Item = apps.get_model("products", "Item")
    db_alias = schema_editor.connection.alias
    Item.objects.using(db_alias).bulk_create([
        Item(size="S", name="스몰", price=7000, isSold=False, menu_id=1),
        Item(size="M", name="미디움", price=7500, isSold=False, menu_id=1),
        Item(size="L", name="라지", price=8000, isSold=False, menu_id=1),
        Item(size="S", name="스몰", price=10000, isSold=False, menu_id=2),
        Item(size="M", name="미디움", price=11000, isSold=False, menu_id=2),
        Item(size="M", name="미디움", price=12000, isSold=False, menu_id=3),
        Item(size="L", name="라지", price=13000, isSold=False, menu_id=3),
        Item(size="M", name="미디움", price=8000, isSold=True, menu_id=4),
        Item(size="L", name="라지", price=7000, isSold=True, menu_id=5),
        Item(size="S", name="스몰", price=8000, isSold=True, menu_id=7),
    ])
    Tag = apps.get_model("products", "Tag")
    db_alias = schema_editor.connection.alias
    Tag.objects.using(db_alias).bulk_create([
        Tag(name="샐러드", type="샐러드", menu_id=1),
        Tag(name="샐러드", type="샐러드", menu_id=2),
        Tag(name="샐러드", type="샐러드", menu_id=3),
        Tag(name="샐러드", type="샐러드", menu_id=4),
        Tag(name="우유", type="우유", menu_id=5),
        Tag(name="우유", type="우유", menu_id=6),
        Tag(name="우유", type="우유", menu_id=7),
        Tag(name="계란", type="계란", menu_id=8),
        Tag(name="계란", type="계란", menu_id=9),
        Tag(name="계란", type="계란", menu_id=10),
    ])


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('salad', 'SALAD'), ('milk', 'MILK'), ('egg', 'EGG')], max_length=30)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('isSold', models.BooleanField(default=False)),
                ('badge', models.CharField(choices=[('new', 'NEW'), ('old', 'OLD')], default='old', max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.menu')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('size', models.CharField(choices=[('L', 'L'), ('M', 'M'), ('S', 'S')], max_length=10)),
                ('price', models.IntegerField(default=0)),
                ('isSold', models.BooleanField(default=False)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.menu')),
            ],
        ),
        migrations.RunPython(set_initial_product_data),
    ]
