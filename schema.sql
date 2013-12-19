CREATE TABLE matches (
	id INT AUTO_INCREMENT,
	title TEXT,
	net_code TEXT,
	ip TEXT,
	timezone TEXT,
	unique_key TEXT,
	created_on DATETIME,
	password TEXT,
	primary key (id)
);
