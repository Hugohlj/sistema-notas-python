create database sistema_nota;
use sistema_nota;

create table alunos(
id int auto_increment primary key,
nome text (100) NOT NULL,
matricula varchar (20) unique NOT NULL
);
create table funcionario(
id int auto_increment primary key,
nome varchar (100) not null,
cpf varchar (15) unique not null,
senha varchar (100)  not null
);



create table notas (
id int auto_increment primary key,
aluno_id int not null,
disciplina varchar (100) not null,
nota decimal (10,2) not null,
foreign key(aluno_id) references alunos(id),
funcionario_id int not null,
foreign key (funcionario_id) references funcionario(id)
);