from django.db.models.signals import post_save
from django.dispatch import receiver
from delivery_note.models import DeliveryNote
from orders.models import Order

@receiver(post_save, sender=DeliveryNote)
def assign_delivery_note_to_order(sender, instance, created, **kwargs):
    if instance.value is not None and instance.order is None:
        order, created_order = Order.objects.get_or_create(
            status=0,
            up=instance.up,
            loading_date=instance.loading_date,
            packages_type=instance.package_type,
            defaults={
                'plant': instance.plant,
                'unloading_date': instance.unloading_date,
                'terms_of_delivery': 'FCA',
                'package_count': instance.package_count,
                'height': instance.total_height,
                'weight': instance.total_weight,
                'ldm': 0,

            }
        )

        if not created_order:
            order.package_count += instance.package_count
            order.height += instance.total_height
            order.weight += instance.total_weight
            order.save(update_fields=['package_count', 'height', 'weight'])

        order.calculate_ldm()
        instance.order = order
        instance.save(update_fields=["order"])

    elif (instance.value is None or instance.value == 0) and instance.order is not None:
        order = instance.order

        # Намаляваме стойностите в Order, свързани с DeliveryNote
        order.package_count -= instance.package_count
        order.height -= instance.total_height
        order.weight -= instance.total_weight

        # Пресмятаме отново LDM след премахването на DeliveryNote
        order.calculate_ldm()

        # Премахваме връзката между DeliveryNote и Order
        instance.order = None
        instance.value = None
        instance.save(update_fields=["order"])

        # Записваме промените в Order
        order.save(update_fields=['package_count', 'height', 'weight', 'ldm'])