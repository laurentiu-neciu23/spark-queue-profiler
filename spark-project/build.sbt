scalafmtOnCompile in Compile := true

resolvers += "Spark Packages Repo" at "http://dl.bintray.com/spark-packages/maven"

organization := "org.spark.laur"
name := "spark-laur"

version := "0.28.0"
crossScalaVersions := Seq("2.11.12", "2.12.7")
scalaVersion := "2.11.12"
sparkVersion := "2.4.0"

libraryDependencies += "org.apache.spark" %% "spark-sql" % "2.4.0" % "provided"
libraryDependencies += "org.apache.spark" %% "spark-mllib" % "2.4.0" % "provided"
libraryDependencies += "edu.stanford.nlp" % "stanford-corenlp" % "3.6.0",
libraryDependencies += "edu.stanford.nlp" % "stanford-corenlp" % "3.6.0" classifier "models",
libraryDependencies += "com.google.protobuf" % "protobuf-java" % "2.6.1"

// All Spark Packages need a license
licenses := Seq("MIT" -> url("http://opensource.org/licenses/MIT"))

javaOptions ++= Seq("-Xms512M", "-Xmx2048M", "-XX:+CMSClassUnloadingEnabled","-Duser.timezone=GMT")
