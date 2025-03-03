CREATE TABLE `db`.`Customer` (
  id_customer INTEGER PRIMARY KEY NOT NULL,
  email VARCHAR(254), 
  nombre VARCHAR(50),
  apellido VARCHAR(50),
  sexo CHAR(1), --M, F, X
  direccion VARCHAR(255),
  fecha_nacimiento DATE,
  telefono VARCHAR(20),
  fecha_registro TIMESTAMP,
  categoria_cliente VARCHAR(20),
  estado_cuenta BOOL
  );

CREATE TABLE `db`.`Seller` (
  id_seller INTEGER PRIMARY KEY NOT NULL,
  nombre VARCHAR(50),
  apellido VARCHAR(50),
  direccion VARCHAR(255),
  fecha_nacimiento DATE,
  entidad VARCHAR(50),
  telefono VARCHAR(20),
  categoria_vendedor VARCHAR(20),
  estado_cuenta BOOL
);

CREATE TABLE `db`.`Item` (
  id_item INTEGER PRIMARY KEY NOT NULL,
  nombre_producto VARCHAR(50),
  descripcion_producto VARCHAR(255),
  precio DECIMAL(10,2),
  estado BOOL ,
  fecha_baja TIMESTAMP,
  ultima_fecha_act TIMESTAMP,
  id_category INTEGER
);

CREATE TABLE `db`.`Order` (
  id_order INTEGER PRIMARY KEY NOT NULL,
  id_category INTEGER -- FK
  id_item INTEGER -- FK
  id_customer INTEGER -- FK
  id_seller INTEGER -- FK
  fecha_transaccion TIMESTAMP
  cantidad_unidades INTEGER 
  monto_total DECIMAL(10,2)
  FOREING KEY (id_customer) REFERENCES Customer(id_customer)
  FOREING KEY (id_seller) REFERENCES Seller(id_seller)
  FOREING KEY (id_item) REFERENCES Item(id_item)
  FOREING KEY (id_category) REFERENCES Category(id_category)
);

CREATE TABLE `db`.`Category` (
  id_category INTEGER PRIMARY KEY NOT NULL,
  id_item INTEGER -- FK
  id_order INTEGER -- FK
  descripcion_categoria VARCHAR(255)
  path VARCHAR(255)
  fecha_alta TIMESTAMP 
  FOREING KEY (id_order) REFERENCES Order(id_order)
);

CREATE TABLE `db`.`Customer_history` (
  id_modificacion INTEGER PRIMARY KEY NOT NULL,
  id_customer INTEGER -- FK
  tipo_modificacion VARCHAR(50) --insert nuevo cliente, update ya existente, delete cliente
  valor_viejo VARCHAR(255) --(json, por ejemplo { ‘email’: ‘old_mail@gmail.com’, ‘telefono’:’44-44’, ‘categoria’:’bronze’})
  valor_nuevo VARCHAR(255) --(json, por ejemplo { ‘email’: ‘new_mail@gmail.com’, ‘telefono’:’45-55’, ‘categoria’:’plata})
  fecha_modificacion TIMESTAMP
  FOREING KEY (id_customer) REFERENCES Customer(id_customer)
);

CREATE TABLE `db`.`Seller_history` (
  id_modificacion INTEGER PRIMARY KEY NOT NULL,
  id_seller INTEGER -- FK
  tipo_modificacion VARCHAR(50) //insert nuevo cliente, update ya existente, delete cliente
  valor_viejo VARCHAR(255) --(json, por ejemplo { ‘email’: ‘old_mail@gmail.com’, ‘telefono’:’44-44’, ‘categoria’:’bronze’})
  valor_nuevo VARCHAR(255) --(json, por ejemplo { ‘email’: ‘new_mail@gmail.com’, ‘telefono’:’45-55’, ‘categoria’:’plata})
  fecha_modificacion TIMESTAMP
  FOREING KEY (id_seler) REFERENCES Seller(id_seler)
);

CREATE TABLE `db`.`Item_history`(
  id_modificacion INTEGER PRIMARY KEY NOT NULL,
  id_item INTEGER --FK
  tipo_modificacion VARCHAR(50) --insert nuevo cliente, update ya existente, delete cliente
  valor_viejo VARCHAR(255) --(json, por ejemplo { ‘email’: ‘old_mail@gmail.com’, ‘telefono’:’44-44’, ‘categoria’:’bronze’})
  valor_nuevo VARCHAR(255) --(json, por ejemplo { ‘email’: ‘new_mail@gmail.com’, ‘telefono’:’45-55’, ‘categoria’:’plata})
  fecha_modificacion TIMESTAMP
  FOREING KEY (id_item) REFERENCES Item(id_item)
);

CREATE TABLE `db`.`Category_history` (
  id_modificacion INTEGER PRIMARY KEY NOT NULL,
  id_category INTEGER --FK
  tipo_modificacion VARCHAR(50) --insert nuevo cliente, update ya existente, delete cliente
  valor_viejo VARCHAR(255) --(json, por ejemplo { ‘email’: ‘old_mail@gmail.com’, ‘telefono’:’44-44’, ‘categoria’:’bronze’})
  valor_nuevo VARCHAR(255) --(json, por ejemplo { ‘email’: ‘new_mail@gmail.com’, ‘telefono’:’45-55’, ‘categoria’:’plata})
  fecha_modificacion TIMESTAMP
  FOREING KEY (id_category) REFERENCES Category(id_category)
);

-- Se podria agregar una columna que relacione esta tabla con el vendedor y comprador
-- para poder realizar un analisis sobre quien vendio o compro mas el articulo X
CREATE TABLE `db`.`Item_status` (
  id_item INTEGER PRIMARY KEY NOT NULL,
  fecha DATE,
  ultimo_precio_registrado DECIMAL(10,2),
  cantidad_vendida INT,
  estado BOOL
);