<%@ page language="java" import="java.sql.*" contentType="text/html;charset=gb2312"%>
<html>
<body>
<%
	request.setCharacterEncoding("utf-8");
	Class.forName("com.mysql.jdbc.Driver");
	String url = "jdbc:mysql://localhost:3306/book?characterEncoding=UTF-8";
	String user = "user";
	String password = "123456";
	Connection conn = null;
	conn = DriverManager.getConnection(url, user, password);
	String t = request.getParameter("token");
	String id = request.getParameter("id");
	
	String sql_search = "SELECT * FROM id_name WHERE id = " + "'"+id+"'" ;
	Statement stmt = conn.createStatement();
	ResultSet rs = stmt.executeQuery(sql_search);
	
	
	if(rs!=null)
	{
		String del="delete from id_name where id = " + "'"+id+"'";
		stmt.executeUpdate(del);
		String sql="insert into id_name(id,token) values(?,?)";
		PreparedStatement stmt_insert=conn.prepareStatement(sql);
		stmt_insert.setString(1,id);
		stmt_insert.setString(2,t);
		stmt_insert.executeUpdate();
	}
	else
	{
		String sql="insert into id_name(id,token) values(?,?)";
		PreparedStatement stmt_insert=conn.prepareStatement(sql);
		stmt_insert.setString(1,id);
		stmt_insert.setString(2,t);
		stmt_insert.executeUpdate();
	}
	
	String sql_selectall = "select * from id_name";
	ResultSet rs_all = stmt.executeQuery(sql_selectall);
	while(rs_all.next())
	{
		String tmpid = rs_all.getString("id");
		String tmpt = rs_all.getString("token");
		out.println("id="+tmpid+" "+"token="+tmpt+"<br>");
	}
 %>
</body>
</html>
