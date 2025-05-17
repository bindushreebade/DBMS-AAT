from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def add_product(id: int, name: str, price: float):
    try:
        data = {"id": id, "name": name, "price": price}
        response = supabase.table("product").insert(data).execute()
        print("✅ Product added:", response.data)
    except Exception as e:
        print("❌ Error adding product:", e)


def delete_product(product_id: int):
    try:
        # First check if product exists
        existing_product = supabase.table("product").select("*").eq(
            "id", product_id).execute()

        if not existing_product.data:
            print(f"❌ Product with ID {product_id} not found.")
            return False

        # Delete the product
        response = supabase.table("product").delete().eq("id",
                                                         product_id).execute()

        if response.data:
            print(f"✅ Product with ID {product_id} deleted successfully.")
            return True
        else:
            print(f"❌ Failed to delete product with ID {product_id}.")
            return False

    except Exception as e:
        print(f"❌ Error deleting product: {e}")
        return False


def list_products():
    try:
        response = supabase.table("product").select("*").execute()
        products = response.data
        if not products:
            print("No products found.")
        else:
            for product in products:
                print(
                    f"🆔 {product['id']} | 🛒 {product['name']} | 💰 ₹{product['price']}"
                )
    except Exception as e:
        print("❌ Error fetching products:", e)


def update_product_price(product_id: int, new_price: float):
    try:
        response = supabase.table("product").select("*").eq(
            "id", product_id).execute()
        if not response.data:
            print("❌ Product not found.")
        else:
            update_response = supabase.table("product").update({
                "price":
                new_price
            }).eq("id", product_id).execute()
            print("✅ Price updated:", update_response.data)
    except Exception as e:
        print("❌ Error updating product:", e)


def apply_discount(percentage: float):
    try:
        discount_factor = 1 - (percentage / 100)
        # Fetch all products
        response = supabase.table("product").select("*").execute()
        products = response.data

        if products:
            for product in products:
                product_id = product["id"]
                new_price = product["price"] * discount_factor

                # Update each product with the new price
                update_response = supabase.table("product").update({
                    "price":
                    new_price
                }).eq("id", product_id).execute()
                if update_response.data is None:
                    print(
                        f"❌ Error updating product {product_id}: {update_response.data}"
                    )
                else:
                    print(
                        f"✅ Product {product_id} price updated to {new_price}")

            print(f"✅ {percentage}% discount applied to all products.")
        else:
            print("No products found to apply discount.")

    except Exception as e:
        print("❌ Error applying discount:", e)
